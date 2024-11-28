import telebot

def num_button():
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = telebot.types.KeyboardButton('Отправить контакт', request_contact=True)
    markup.add(button)
    return markup
