import os
import sqlite3

from telebot.types import Message


SQL_INSERT_MESSAGE = """
INSERT INTO messages (user_id, message)
              VALUES (?, ?)
"""


conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "bot.db"))
cursor = conn.cursor()


def insert_message(message: Message):
    sender_id = str(message.from_user.id)

    cursor.execute(SQL_INSERT_MESSAGE, (sender_id, str(message.json)))
    conn.commit()


def _init_db():
    init_db_path = os.path.join(os.path.dirname(__file__), "init_db.sql")
    with open(init_db_path, "r") as queries_file:
        sql = queries_file.read()
    cursor.executescript(sql)
    conn.commit()


_init_db()
