from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
import config
import gpt
from threading import Thread
bot = TeleBot(config.TOKEN)
MAX_LETTERS = config.MAX_TOKENS
import sqlite
import sqlite3
smiles = "🐍📵🤖👾👽👻🧞‍♂️™🚩"

ai_desc = {
    "Математик": ["Ты дружулюбный помошник по математике и даешь простые ответы", "Ты дружулюбный помошник по математике и даешь сложные ответы"],
    "Шефповр": ["Ты повор, ты помогаешь всем простым рецептом","Ты повор, ты помогаешь всем простым рецептом"],
    "Программист": ["Ты программист, ты помогаешь всем с написанием простого кода", "Ты программист, ты помогаешь всем с написанием сложного кода"],
    "Историк": ["Ты историк ,ответишьна вопрос по любой дате и расскажешь о ней как маленькому ребенку", "Ты историк ,ответишьна вопрос по любой дате и расскажешь о ней как профессору"]
}

# Функция для создания клавиатуры с нужными кнопочками
def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard


# Приветственное сообщение /start
@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f"Привет, {user_name}! Я бот-помощник для написание кода на Python!🐍📵\n"
                          f"Ты можешь прислать условие  а я постараюсь ниписать тебе код)🤖👾.\n"
                          "Иногда ответы получаются слишком длинными - в этом случае ты можешь попросить продолжить.",
                     reply_markup=create_keyboard(["/let`s_go", '/help', '/addition', '/stop']))
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    sqlite.prepare_database()
    cur.execute(f"SELECT user_id FROM questions WHERE user_id = {id}")
    if cur.fetchone() is None:
        sqlite.start_regestration(message)

@bot.message_handler(commands=["let`s_go"])
def complexity(message):
    bot.send_message(message.chat.id, "Выберите уровень сложности)", reply_markup=create_keyboard(["/junior", "/senior"]))

@bot.message_handler(commands=["junior"])
def junior_roll(message):
    bot.send_message(message.chat.id, "Прошу выбери специальность бота:",
                     reply_markup=create_keyboard(["powar_chat", "IT_chat", "math_chat", "history_chat"]))

    bot.register_next_step_handler(message, get_answer_regulation_junior)

@bot.message_handler(commands=["senior"])
def senior_roll(message):
    bot.send_message(message.chat.id, "Прошу выбери специальность бота:",
                     reply_markup=create_keyboard(["powar_chat", "IT_chat", "math_chat", "history_chat"]))
    bot.register_next_step_handler(message, get_answer_regulation_senior)

# Команда /help
@bot.message_handler(commands=['help'])
def support(message):
    bot.send_message(message.from_user.id,
                     text="Чтобы приступить к решению задачи: нажми /let`s_go, выбери направленность бота, а затем напиши условие задачи")
def get_answer_regulation_senior(message):
    id = message.from_user.id
    if message.text == "powar_chat":
        system_content_1 = ai_desc["Шефповр"][1]
    elif message.text == "IT_chat":
        system_content_1 = ai_desc["Программист"][1]
    elif message.text == "math_chat":
        system_content_1 = ai_desc["Математик"][1]
    elif message.text == "history_chat":
        system_content_1 = ai_desc["Историк"][1]
    else:
        bot.send_message(message.chat.id, "Начните процедуру сначала видимо что-то пошло не так")
    t1 = Thread(target=sqlite.neeronka_answers_regulation(system_content_1, id))
    t2 = Thread(target=bot.register_next_step_handler(message, create_promt_and_work))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
def get_answer_regulation_junior(message):
    id = message.from_user.id
    if message.text == "powar_chat":
        system_content_1 = ai_desc["Шефповр"][0]
    elif message.text == "IT_chat":
        system_content_1 = ai_desc["Программист"][0]
    elif message.text == "math_chat":
        system_content_1 = ai_desc["Математик"][0]
    elif message.text == "history_chat":
        system_content_1 = ai_desc["Историк"][0]
    else:
        bot.send_message(message.chat.id, "Начните процедуру сначала видимо что-то пошло не так")
    t1 = Thread(target=sqlite.neeronka_answers_regulation(system_content_1, id))
    t2 = Thread(target=for_promt(message))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def create_promt_and_work(message):
    id = message.from_user.id
    promt = message.text
    user_id = message.from_user.id
    if message.content_type != "text":
        bot.send_message(message.chat.id, "Необходимо отправить именно текстовое сообщение")
        bot.register_next_step_handler(message, create_promt_and_work)

    if len(message.text) > MAX_LETTERS:
        bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
        bot.register_next_step_handler(message, create_promt_and_work)
    else:
        bot.send_message(message.chat.id, "Ваш промт уже отправлен GPT, ожидайте ответа!)")
        #sqlite.add_or_update_promt(promt, id)
        #bot.register_next_step_handler(message, gpt.GPT_message_generate)
        t1 = Thread(target=sqlite.add_or_update_promt(promt, id))
        t2 = Thread(target=gpt.GPT_message_generate(message))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
@bot.message_handler(commands=['addition', "additio"])
def addition_prompt(message):
    id = message.chat.id
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    results = cur.execute(f'SELECT answer FROM questions WHERE user_id = {id};')
    for res in results:
        task = res[0]
    if task != None or task != "":
        bot.send_message(message.chat.id, "P.s. Если что, я могу продолжать решение только последней задачи! А точнее продолжение появится прямо сейчас, я активно над ним работаю)")
        bot.register_next_step_handler(message, gpt.addition_GPT)
    else:
        bot.send_message(message.chat.id, "Чтобы запросить дополнение, нужно иметь готовый ответ от нееросети!\n Функция создания промта включена")
        bot.register_next_step_handler(message, for_promt)


@bot.message_handler(commands=["stop_gnenerate"])
def stop_generate(message):
    id = message.from_user.id
    gpt.error_or_stop(id)

def for_promt(message):
    bot.send_message(message.chat.id, "Напиши условие новой задачи:")
    bot.register_next_step_handler(message, create_promt_and_work)
bot.polling()
