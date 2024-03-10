import sqlite3
import telebot
import config
bot = telebot.TeleBot(config.TOKEN)

a = None
def prepare_database():
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()

    query = (f'CREATE TABLE IF NOT EXISTS questions' \
                    f'(user_id INTEGER PRIMARY KEY, ' \
                    f'name TEXT, ' \
                    f'system_content TEXT, ' \
                    f'task TEXT, ' \
                    f'answer TEXT)')

    cur.execute(query)
    connection.commit()
    cur.close()
    pass
def start_regestration(message):
    id = message.from_user.id
    name = message.from_user.first_name
    first_info = (id, name)
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute(
        f'INSERT INTO questions (user_id, name) VALUES (?, ?);', first_info)
    connection.commit()
    cur.close()
    pass

def add_or_update_promt(promt, id):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute(f'UPDATE questions SET task = ? WHERE user_id = ?;',(f"{promt}", id))
    connection.commit()
    cur.close()
    pass

def add_or_update_answer(answer, id):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute(f'UPDATE questions SET answer = ? WHERE user_id = ?;', (f"{answer}", id))
    connection.commit()
    cur.close()
    pass

def neeronka_answers_regulation(system_content_1, id):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute(f'UPDATE questions SET system_content = ? WHERE user_id = ?;', (f"{system_content_1}", id))
    connection.commit()
    cur.close()
    pass















