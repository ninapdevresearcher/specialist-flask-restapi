from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
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
   quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

   # QuoteModel - связываемся с этой табл,
   # backref - обратная связь: у автора есть цитаты, а у цитаты будет автор
   # lazy - параметр, кот управляет запросами более чем в 1 табл (join)

   def __init__(self, name):
       self.name = name

   def to_dict(self):
       return {
           "id": self.id,
           "name": self.name
       }


class QuoteModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
   text = db.Column(db.String(255), unique=False)

   def __init__(self, author, text):
       self.author_id = author.id
       self.text = text

   def to_dict(self):
       return {
           "id": self.id,
           "name": self.text,
           "author": self.author.to_dict() #связанный параметр
       }



@app.errorhandler(404)
def handler_bad_request(error):
    return "A quote with such parameters was not found", 404


#Author
#--------------------------------------------------------------------------
#Создаем нового автора
@app.post("/authors")
def create_author():
    author_data = request.json
    author = AuthorModel(author_data["name"])
    db.session.add(author)
    db.session.commit()
    return author.to_dict(), 201


#Получаем всех авторов
@app.route("/authors")
def get_authors():
    authors: list[AuthorModel] = AuthorModel.query.all()
    authors_dict: list[dict] = []
    for author in authors:
        authors_dict.append(author.to_dict())
    return authors_dict

#Удаляем автора
@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        abort(404)
    else:
        db.session.delete(author)
        db.session.commit()
        return f"Author with id={author_id} has deleted", 200


# dict -> JSON - сериализация
# JSON -> dict - десериализация
# Object -> dict (функция) -> JSON (фреймворк)
# http://127.0.0.1:5000/quotes
@app.route("/quotes")
def get_quotes():
    quotes: list[QuoteModel] = QuoteModel.query.all()
    quotes_dict: list[dict] = []
    for quote in quotes:
        quotes_dict.append(quote.to_dict())
    return quotes_dict

#Получаем цитату по id
# http://127.0.0.1:5000/quotes/1
@app.route("/quotes/<int:quote_id>")  # шаблон урла
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404)
    return quote.to_dict()

#Создаем цитату
@app.route("/authors/<int:author_id>/quotes", methods=["POST"])
def create_quote(author_id):
    author = AuthorModel.query.get(author_id)
    new_quote = request.json
    quote = QuoteModel(author, **new_quote) #распаковка через **
    db.session.add(quote)
    db.session.commit()
    return quote.to_dict(), 201




# @app.route("/quotes/<int:quote_id>", methods=["PUT"])
# def edit_quote(quote_id):
#     new_quote = request.json
#     author = new_quote['author']
#     text = new_quote['text']
#     if len(author) == 0 and len(text) == 0:
#         return "Add a new text or author to edit the quote", 400
#     else:
#         conn = get_db()
#         if len(author) == 0:
#             sql = f"UPDATE quotes SET text = '{text}' WHERE id = {quote_id};"
#         elif len(text) == 0:
#             sql = f"UPDATE quotes SET author = '{author}' WHERE id = {quote_id};"
#         else:
#             sql = f"UPDATE quotes SET author = '{author}', text = '{text}' WHERE id = {quote_id};"
#         cursor = conn.cursor().execute(sql)
#         conn.commit()
#         result = cursor.rowcount
#         cursor.close()
#         if result == 1:
#             return new_quote
#             # return f"Quote with id {quote_id} changed.", 200
#         else:
#             return abort(404)
#
# @app.route("/quotes/<quote_id>", methods=['DELETE'])
# def delete(quote_id):
#     conn = get_db()
#     sql = f"DELETE FROM quotes WHERE id = {quote_id};"
#     cursor = conn.cursor().execute(sql)
#     conn.commit()
#     result = cursor.rowcount
#     cursor.close()
#     if result == 1:
#         return f"Quote with id {quote_id} is deleted.", 200
#     else:
#         return abort(404)


if __name__ == "__main__":
    app.run(debug=True)

