from flask import Flask, json, request, abort
from flask import g
import random
import sqlite3
from pathlib import Path

app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / 'test.db'


# Функции автоматизации повторяющихся кусков
def tuple_to_dict(quote: tuple) -> dict:
    keys = ["id", "author", "text"]
    return dict(zip(keys, quote))


def get_db():  # проверяем есть ли соединение, если нет - устанавливаем
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext  # закрываем соединение
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(404)
def handler_bad_request(error):
    return "A quote with such parameters was not found", 404


def get_object_from_db(sql: str): #, quote_id: int):
    conn = get_db()  # Подключение в БД
    cursor = conn.cursor().execute(sql)  # Создаем cursor, он позволяет делать SQL-запросы и Выполняем запрос
    object = cursor.fetchone()  # Извлекаем результаты запроса
    cursor.close()  # Закрыть курсор:
    # conn.close()  # Закрыть соединение:
    if object is None:
        abort(404)
    else:
        object = tuple_to_dict(object)
        return object


def get_objects_from_db(sql: str) -> list[dict]:
    conn = get_db()
    cursor = conn.cursor().execute(sql)
    objects = cursor.fetchall()
    cursor.close()
    # conn.close()
    if object is None:
        abort(404)
    else:
        objects = list(map(tuple_to_dict, objects))
        return objects


# --------------------------------------------------------------------------------
# Функции к запросам
# http://127.0.0.1:5000/quotes
@app.route("/quotes")
def get_quotes():
    select_quotes = "SELECT * from quotes"
    quotes = get_objects_from_db(select_quotes)
    return quotes


# http://127.0.0.1:5000/quotes/1
@app.route("/quotes/<int:quote_id>")  # шаблон урла
def get_quote_by_id(quote_id):
    sql = f"SELECT * FROM quotes WHERE id={quote_id}"
    quote = get_object_from_db(sql)
    return quote


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_qoute = request.json
    if len(new_qoute['author']) == 0 or len(new_qoute['text']) == 0:
        return "Add a quote author and text to create new quote!", 400
    else:
        conn = get_db()  # функци подключения к бд из док-ии
        sql = f"INSERT INTO quotes(author, text) VALUES('{new_qoute['author']}', '{new_qoute['text']}');"
        cursor = conn.cursor().execute(sql)
        conn.commit()
        new_qoute["id"] = cursor.lastrowid  # получаем id нового объекта
        cursor.close()
        return new_qoute, 201

@app.route("/quotes/<int:quote_id>", methods=["PUT"])
def edit_quote(quote_id):
    new_quote = request.json
    author = new_quote['author']
    text = new_quote['text']
    if len(author) == 0 and len(text) == 0:
        return "Add a new text or author to edit the quote", 400
    else:
        conn = get_db()
        if len(author) == 0:
            sql = f"UPDATE quotes SET text = '{text}' WHERE id = {quote_id};"
        elif len(text) == 0:
            sql = f"UPDATE quotes SET author = '{author}' WHERE id = {quote_id};"
        else:
            sql = f"UPDATE quotes SET author = '{author}', text = '{text}' WHERE id = {quote_id};"
        cursor = conn.cursor().execute(sql)
        conn.commit()
        result = cursor.rowcount
        cursor.close()
        if result == 1:
            return new_quote
            # return f"Quote with id {quote_id} changed.", 200
        else:
            return abort(404)


@app.route("/quotes/<quote_id>", methods=['DELETE'])
def delete(quote_id):
    conn = get_db()
    sql = f"DELETE FROM quotes WHERE id = {quote_id};"
    cursor = conn.cursor().execute(sql)
    conn.commit()
    result = cursor.rowcount
    cursor.close()
    if result == 1:
        return f"Quote with id {quote_id} is deleted.", 200
    else:
        return abort(404)


# # http://127.0.0.1:5000/quotes/count
# @app.route("/quotes/count")
# def count_quotes():
#     return {
#         'count': len(quotes)
#          }


# # http://127.0.0.1:5000/quotes/random
# @app.route("/quotes/random")
# def get_random_quote():
#     return random.choice(quotes)
