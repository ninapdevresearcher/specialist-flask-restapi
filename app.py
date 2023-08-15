from flask import Flask, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import false
from flask_migrate import Migrate
from pathlib import Path


BASE_DIR = Path(__file__).parent
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AuthorModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32), unique=True)
   surname = db.Column(db.String(32), nullable=True)
   __table_args__ = (db.UniqueConstraint('name', 'surname'),) #не работает из-за unique в name, compate_type в env.py не помог
   quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic', cascade="all, delete-orphan")
   is_deleted = db.Column(db.Boolean, unique=False, default=False, server_default=false())

   # QuoteModel - связываемся с этой табл,
   # backref - обратная связь: у автора есть цитаты, а у цитаты будет автор
   # lazy - параметр, кот управляет запросами более чем в 1 табл (join)

   def __init__(self, name, surname=None):
       self.name = name
       self.surname = surname


   def to_dict(self):
       return {
           "id": self.id,
           "name": self.name,
           "surname": self.surname,
           "is_deleted": self.is_deleted
       }


class QuoteModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
   text = db.Column(db.String(255), unique=False)
   created = db.Column(db.DateTime(timezone=True), server_default=func.now())
   rating = db.Column(db.Integer, nullable=False, default='1', server_default='1')

   def __init__(self, author, text, created=func.now(), rating=1):
       self.author_id = author.id
       self.text = text
       self.created = created
       self.rating = rating

   def to_dict(self):
       return {
           "id": self.id,
           "text": self.text,
           "author": self.author.to_dict(), #связанный параметр
           "rating": self.rating,
           "created": self.created
       }


@app.errorhandler(404)
def handler_bad_request(error):
    return "A quote or author with such parameters was not found", 404


#Author
#--------------------------------------------------------------------------
#Author. Get by id
@app.route("/authors/<int:author_id>")
def get_author_by_id(author_id):
    author = AuthorModel.query.filter_by(is_deleted=False, id=author_id).first()
    if author is None:
        abort(404)
    return author.to_dict()

#Author. Get all
@app.route("/authors")
def get_authors():
    authors: list[AuthorModel] = AuthorModel.query.filter_by(is_deleted=False).all()
    authors_dict: list[dict] = [author.to_dict() for author in authors]
    return authors_dict

#Author. Create
@app.post("/authors")
def create_author():
    author_data = request.json
    name = author_data["name"]
    author = AuthorModel(name)
    if len(author_data["surname"]) != 0:
        surname = author_data["surname"]
        author = AuthorModel(name, surname)
    db.session.add(author)
    db.session.commit()
    return author.to_dict(), 201

#Author. Edit
@app.put("/authors/<int:author_id>")
def edit_author(author_id):
    author_data = request.json
    author = AuthorModel.query.filter_by(is_deleted=False, id=author_id).first()
    if author is None:
        abort(404)
    for key, value in author_data.items():
        setattr(author, key, value)
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_dict()), 200

#Author. Full delete
@app.delete("/authors/<int:author_id>/delete")
def full_delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        abort(404)
    db.session.delete(author)
    db.session.commit()
    return f"Author with id={author_id} has really been deleted", 200

#Author. Soft delete
@app.delete("/authors/<int:author_id>")
def sort_delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        abort(404)
    author.is_deleted = True
    db.session.commit()
    return f"Author with id={author_id} has deleted", 200

#Author. Recover all author
@app.put("/authors/recover/all")
def recover_all_authors():
    authors: list[AuthorModel] = AuthorModel.query.filter_by(is_deleted=True).all()
    if len(authors) == 0:
        abort(404)
    authors_dict: list[dict] = []
    for author in authors:
        author.is_deleted = False
        db.session.commit()
        authors_dict.append(author.to_dict())
    return authors_dict

#Author. Recover author by author_id
@app.put("/authors/recover/<int:author_id>")
def recover_author_by_id(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        abort(404)
    author.is_deleted = False
    db.session.commit()
    return f"Author with id={author_id} has recovered", 200

#Quotes
#-------------------------------------------------------------------------------
# dict -> JSON - сериализация
# JSON -> dict - десериализация
# Object -> dict (функция) -> JSON (фреймворк)

#Quote. Get all quotes
# http://127.0.0.1:5000/quotes
@app.route("/quotes")
def get_quotes():
    quotes: list[QuoteModel] = QuoteModel.query.all()
    quotes_dict: list[dict] = [quote.to_dict() for quote in quotes]
    return quotes_dict

#Quote. Get by id
# http://127.0.0.1:5000/quotes/1
@app.route("/quotes/<int:quote_id>")  # шаблон урла
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404)
    return quote.to_dict()

#Quote. Get all author`s quotes
# http://127.0.0.1:5000/authors/2/quotes
@app.route("/authors/<int:author_id>/quotes")
def get_all_quotes_by_author(author_id):
    quotes: list[QuoteModel] = QuoteModel.query.filter_by(author_id=f"{author_id}")
    quotes_dict: list[dict] = [quote.to_dict() for quote in quotes]
    if len(quotes_dict) == 0:
        abort(404)
    return quotes_dict

#Quote. Create
@app.route("/authors/<int:author_id>/quotes", methods=["POST"])
def create_quote(author_id):
    author = AuthorModel.query.get(author_id)
    new_quote = request.json
    rating = int(new_quote['rating'])
    if rating > 5:
        new_quote['rating'] = '5'
    elif rating <= 0:
        new_quote['rating'] = '1'
    quote = QuoteModel(author, **new_quote) #распаковка через **
    db.session.add(quote)
    db.session.commit()
    return quote.to_dict(), 201

#Quote. Edit
@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id):
    new_quote = request.json
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404)
    quote.text = new_quote["text"]
    db.session.commit()
    return jsonify(quote.to_dict()), 200
#добавить
    # for key, value in author_data.items():
    #     setattr(author, key, value)
    # db.session.add(author)
    # db.session.commit()
    # return jsonify(author.to_dict()), 200

@app.delete("/quotes/<int:quote_id>")
def delete_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404)
    else:
        db.session.delete(quote)
        db.session.commit()
        return f"Quote with id={quote_id} has deleted", 200


#Over requests of filters
#-------------------------------------------------------------------------------
@app.get("/quotes/<int:quote_id>/increase_rating")
def increase_rating(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404)
    if quote.rating < 5:
        quote.rating += 1
        db.session.commit()
        return jsonify(quote.to_dict()), 200
    return f"Rating for quote {quote_id} is maxed out", 200
    
@app.get("/quotes/<int:quote_id>/decrease_rating")
def decrease_rating(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404)
    if quote.rating > 1:
        quote.rating -= 1
        db.session.commit()
        return jsonify(quote.to_dict()), 200
    return f"rating for quote {quote_id} is minumum", 200

#Получаем всех авторов с именем или с двумя (ПР, Nina)
# http://127.0.0.1:5000/authors/filters?name=nina
@app.get("/authors/filters")
def get_authors_by():
    name = request.args.get('name', default=None, type=None)
    name2 = request.args.get('name2', default=None, type=None)
    surname = request.args.get('surname', default=None, type=None)
    surname2 = request.args.get('surname2', default=None, type=None)
    authors = AuthorModel.query.filter((AuthorModel.name.ilike(f"%{name}%")) | (AuthorModel.name.ilike(f"%{name2}%")) | (AuthorModel.surname.ilike(f"%{surname}%")) | (AuthorModel.surname.ilike(f"%{surname2}%")))
    author_dict: list[dict] = []
    for author in authors:
        author_dict.append(author.to_dict())
    if len(author_dict) == 0:
        return abort(404)
    return author_dict

# Получаем все цитаты по имени автора и/или с определенным рейтингом
# http://127.0.0.1:5000/quotes/filters?name=rick
# @app.get("/quotes/filters")
# def get_quotes_with_filters():
#     # kwargs = request.args
#     for x, y in request.args.items():
#         quotes = QuoteModel.query.join(QuoteModel.author).filter(QuoteModel.f"{x}".ilike(f"%{y}%")) #**kwargs)
#         if quotes:
#             result = [quote.to_dict() for quote in quotes]
#         return jsonify(result), 200
    # except:
    #     abort(404)
    #
    # name = kwargs.get('name', default=None, type=None)
    # surname = kwargs.get('surname', default=None, type=None)
    # rating = kwargs.get('rating', default=None, type=None)
    # text = kwargs.get('text', default=None, type=None)
    # quotes = QuoteModel.query.filter((QuoteModel.rating==f"{rating}") | (QuoteModel.text.ilike(f"%{text}%"))
    # #(QuoteModel.author.has(name=f"%{name}%")) | (QuoteModel.author.has(surname=f"{surname}")) |
    # # quotes = QuoteModel.qu[[[ery.join(QuoteModel.author).filter(QuoteModel.name == 'Tom')
    # quote_dict: list[dict] = []
    # for quote in quotes:
    #     quote_dict.append(quote.to_dict())
    # if len(quote_dict) == 0:
    #     return abort(404)
    # return quote_dict
    #
    #  abort(404)
    # for key, value in author_data.items():
    #     setattr(author, key, value)
    # db.session.add(author)
    # db.session.commit()



#Author. Sorted by name or surname
@app.route("/authors/sortedby/<tag>")
def get_sorted_authors(tag):
    authors: list[AuthorModel] = AuthorModel.query.all()
    authors_dict: list[dict] = [author.to_dict() for author in authors if author.surname is not None]
    if tag == "name":
        authors_dict = sorted(authors_dict, key=lambda x: x['name'])
    elif tag == "surname":
        authors_dict = sorted(authors_dict, key=lambda x: x['surname'])
    return authors_dict

if __name__ == "__main__":
    app.run(debug=True)

