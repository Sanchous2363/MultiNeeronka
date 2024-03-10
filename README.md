# MultiNeeronka
#ФАЙЛЫ В ПРОЕКТЕ:
Название файла  | Содержание файла
----------------|----------------------
config.py       | Хранение top_secret информации
sqlite.py       | хранение данных
gpt.py          | промт gpt, ответ и хранение данных
bot.py          | функции бота

#ЧТО ЗА НЕЙРОНКА:

deepseek-ai_deepseek-coder-6.7b-instruct
![Безымянный](https://github.com/Sanchous2363/Neeronks_bot/assets/151240556/92020a70-5060-4623-a6ec-f6990fd51870)

<details>

<summary>Информация о подключении:</summary>

#ГЛАВНАЯ ОСОБЕННОСТЬ НЕЙРОНКИ: НЕ НУЖЕН КЛЮЧ OPENAI ДЛЯ РАБОТЫ!🐍

```ruby
from openai import OpenAI

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
```

</details>

#ЧТО НОВОГО:
 1. Хранение данных при помощи SQLite
 2. Нескольно направленностей для нееронки

#НОВАЯ ДЛЯ МЕНЯ ФУНКЦИЯ И КАК Я С НЕЙ РАБОТАЛ:

```ruby
from threading import Thread
```
Данная функция нужна чтобы можно было выполнять 2 функции одновременно, при этом они ни как друг другу немешают.
Они начинаются одновременно, но не обязательно должны закончиться в определенное время)

```ruby
t1 = Thread(target=sqlite.neeronka_answers_regulation(system_content_1, id))
    t2 = Thread(target=bot.register_next_step_handler(message, create_promt_and_work))
    t1.start() #Начало первой функции
    t2.start() #Начало второй функции
    t1.join()  #Конец первой функции, не зависимо от окончания 2
    t2.join()  #Конец второй функции, не зависимо от окончания 1
```

#ВСЕ РОЛИ БОТА:

```ruby
ai_desc = {
    "Математик": ["Ты дружулюбный помошник по математике и даешь простые ответы", "Ты дружулюбный помошник по математике и даешь сложные ответы"],
    "Шефповр": ["Ты повор, ты помогаешь всем простым рецептом","Ты повор, ты помогаешь всем простым рецептом"],
    "Программист": ["Ты программист, ты помогаешь всем с написанием простого кода", "Ты программист, ты помогаешь всем с написанием сложного кода"],
    "Историк": ["Ты историк ,ответишьна вопрос по любой дате и расскажешь о ней как маленькому ребенку", "Ты историк ,ответишьна вопрос по любой дате и расскажешь о ней как профессору"]
}
```





