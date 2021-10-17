import telebot
from telebot import types

bot = telebot.TeleBot('2087685317:AAHWV1cRC0jiFKDr0D_5hfxtndHX1rUe_uM')

array_left = 0
array_right = 101


def get_middle():
    v = list(range(array_left, array_right, 1))
    middle_index = int((len(v) - 1) / 2)
    return v[middle_index]


def create_field(call, is_less='='):
    n = get_middle()
    keyboard = types.InlineKeyboardMarkup()
    key_more = types.InlineKeyboardButton(text='Больше', callback_data=f'number_m')
    keyboard.add(key_more)
    key_less = types.InlineKeyboardButton(text='Меньше', callback_data=f'number_l')
    keyboard.add(key_less)
    key_win = types.InlineKeyboardButton(text='Это моё число', callback_data='win')
    keyboard.add(key_win)
    if is_less == '>':
        global array_left
        array_left = n
    elif is_less == '<':
        global array_right
        array_right = n
    bot.send_message(call.message.chat.id, f"Это число {n}?", reply_markup=keyboard)


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
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "start_number":
        create_field(call)
    elif call.data == "win":
        keyboard = types.InlineKeyboardMarkup()
        key_start = types.InlineKeyboardButton(text='Да', callback_data='start_number')
        keyboard.add(key_start)
        key_finish = types.InlineKeyboardButton(text='Нет', callback_data='empty')
        keyboard.add(key_finish)
        bot.send_message(call.message.chat.id, "Хочешь сыграть заново?", reply_markup=keyboard)
    elif call.data == "empty":
        bot.send_message(call.message.chat.id, "Если захочешь сыграть - просто введи /start")
    elif call.data == "number_l":
        create_field(call, '<')
    elif call.data == "number_m":
        create_field(call, '>')


bot.polling(none_stop=True, interval=0)
