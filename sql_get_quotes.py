import sqlite3

select_quotes = "SELECT * from quotes"
connection = sqlite3.connect("test.db") # Подключение в БД
cursor = connection.cursor() # Создаем cursor, он позволяет делать SQL-запросы
cursor.execute(select_quotes) # Выполняем запрос:

# Извлекаем результаты запроса
quotes = cursor.fetchall()
print(f"{quotes=}")

cursor.close() # Закрыть курсор:
connection.close() # Закрыть соединение:

