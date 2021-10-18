import telebot
from telebot import types

bot = telebot.TeleBot('2087685317:AAHWV1cRC0jiFKDr0D_5hfxtndHX1rUe_uM')

array_left = 0
array_right = 101
count = 0
presented_number = []


def create_field(call):
    global presented_number
    n = (array_left + array_right) // 2
    if n not in presented_number:
        bot.send_message(call.message.chat.id, f"Это число {n}?", reply_markup=create_keyboard_more_less())
        global count
        count += 1
        presented_number.append(n)
    else:
        bot.send_message(call.message.chat.id, f"Число {n} уже было! Ты про него забыл? Хочешь начать заново?",
                         reply_markup=create_keyboard_ys_no())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет" or message.text.lower() == "/start":
        bot.send_message(message.from_user.id, "Привет, загадай число от 1 до 100 и нажми старт")
        keyboard = types.InlineKeyboardMarkup()
        key_start = types.InlineKeyboardButton(text='Старт', callback_data='start_number')
        keyboard.add(key_start)
        bot.send_message(message.from_user.id, text='Запомни число и начинаем играть!', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет или /start")
    elif message.text == "/stop":
        bot.send_message(message.from_user.id, "Если захочешь поиграть - просто напиши /start")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global array_right
    global array_left
    if call.data == "start_number":
        array_right = 101
        array_left = 0
        create_field(call)
    elif call.data == "win":
        array_right = 101
        array_left = 0
        bot.send_message(call.message.chat.id, "Хочешь сыграть заново?", reply_markup=create_keyboard_ys_no())
    elif call.data == "empty":
        array_right = 101
        array_left = 0
        bot.send_message(call.message.chat.id, "Если захочешь сыграть - просто введи /start")
    elif call.data == "number_l":
        if count < 8:
            n = (array_left + array_right) // 2
            array_right = n - 1
            create_field(call)
        else:
            bot.send_message(call.message.chat.id, "Упс, я проиграл")
    elif call.data == "number_m":
        if count < 8:
            n = (array_left + array_right) // 2
            array_left = n + 1
            create_field(call)
        else:
            bot.send_message(call.message.chat.id, "Упс, я проиграл")


def create_keyboard_ys_no():
    keyboard = types.InlineKeyboardMarkup()
    key_start = types.InlineKeyboardButton(text='Да', callback_data='start_number')
    keyboard.add(key_start)
    key_finish = types.InlineKeyboardButton(text='Нет', callback_data='empty')
    keyboard.add(key_finish)
    return keyboard


def create_keyboard_more_less():
    keyboard = types.InlineKeyboardMarkup()
    key_more = types.InlineKeyboardButton(text='Больше', callback_data=f'number_m')
    keyboard.add(key_more)
    key_less = types.InlineKeyboardButton(text='Меньше', callback_data=f'number_l')
    keyboard.add(key_less)
    key_win = types.InlineKeyboardButton(text='Это моё число', callback_data='win')
    keyboard.add(key_win)
    return keyboard


bot.polling(none_stop=True, interval=0)
