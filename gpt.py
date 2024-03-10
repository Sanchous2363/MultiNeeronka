from openai import OpenAI

import sqlite
from config import MAX_TOKENS, TOKEN
import telebot
import requests
import sqlite3
bot = telebot.TeleBot(TOKEN)
def GPT_message_generate(message):
  id = message.from_user.id
  connection = sqlite3.connect('users.db')
  cur = connection.cursor()
  results = cur.execute(f'SELECT task, system_content FROM questions WHERE user_id = {id};')
  for res in results:
    task = res[0]
    system_content = res[1]

  client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
  assistant_content = "Реши задачу и объясни решение"
  completion = client.chat.completions.create(
    model="local-model",  # this field is currently unused
    messages=[
      {"role": "system", "content": system_content},
      {"role": "user", "content": task},
      {"role": "assistant", "content": assistant_content}
    ],
    temperature=0.7,
    max_tokens=MAX_TOKENS
  )
  response = requests.post("http://localhost:1234/v1")
  try:
    if response.status_code == 200:
      answer = completion.choices[0].message.content
      bot.send_message(message.chat.id, answer + "🐍")
      sqlite.add_or_update_answer(answer, id)
    else:
      bot.send_message(message.chat.id,"Ошибка:", response.text)
      error_or_stop(id)
  except:
    bot.send_message(message.chat.id, "Возможно возникла ошибка при регистрации, прошу начать сначала, данные будут стерты!")
    error_or_stop(id)


def addition_GPT(message):
  id = message.from_user.id
  connection = sqlite3.connect('users.db')
  cur = connection.cursor()
  results = cur.execute(f'SELECT answer, system_content FROM questions WHERE user_id = {id};')
  for res in results:
    task = res[0]
    system_content = res[1]
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
  assistant_content = "Продолжи объяснение:"
  completion = client.chat.completions.create(
    model="local-model",  # this field is currently unused
    messages=[
      {"role": "system",
       "content": system_content},
      {"role": "user", "content": task},
      {"role": "assistant", "content": assistant_content}
    ],
    temperature=0.7,
    max_tokens=MAX_TOKENS
  )
  response = requests.post("http://localhost:1234/v1")
  try:
    if response.status_code == 200:
      answer = completion.choices[0].message.content
      bot.send_message(message.chat.id, f"Доработка к ответу: {answer} + 🐍")
      sqlite.add_or_update_answer(answer, id)
      promt = assistant_content + task
      sqlite.add_or_update_promt(promt, id)
    else:
      bot.send_message(message.chat.id, "Ошибка:", response.text)
      error_or_stop(id)
  except:
    bot.send_message(message.chat.id,
                     "Возможно возникла ошибка при регистрации, прошу начать сначала, данные будут стерты!")
    error_or_stop(id)

def error_or_stop(id):
  system_content_1 = None
  sqlite.neeronka_answers_regulation(system_content_1, id)
  promt = None
  sqlite.add_or_update_promt(promt, id)
  answer = None
  sqlite.add_or_update_answer(answer, id)
