import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()


# Создаем таблицу пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, number TEXT UNIQUE);')



# Проверка user'а на наличие в БД
def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE id=?;', (tg_id,)).fetchone():
        return True
    else:
        return False


## Методы для пользователя ##
# Регистрация
def register(tg_id, name, num):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (tg_id, name, num))
    # Фиксируем изменения
    connection.commit()






connection.commit()