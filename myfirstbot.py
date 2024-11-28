import telebot
from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton
import baza, buttons


bot = telebot.TeleBot('7789806151:AAH_c4A498C_b64NJjZ0vDSJMX7S7BgLLCk')

users = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not baza.check_user(user_id):  # Если пользователь не зарегистрирован
        bot.send_message(user_id, 'Привет! Давай начнем регистрацию!\nНапиши свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(user_id, 'Ты уже зарегистрирован!')
        lang_markup=InlineKeyboardMarkup()
        lang_markup.add()
        InlineKeyboardButton("Русский", callback_data='lang_ru'),
        InlineKeyboardButton("O‘zbekcha", callback_data='lang_uz')

        bot.send_message(user_id, 'Выберите язык / Tilni tanlang:', reply_markup=lang_markup)

# Обработчик выбора языка
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))


def select_language(call):
    user_id = call.from_user.id
    language = call.data.split('_')[1]  # Получаем код языка (ru/uz)
    users[user_id] = {'language': language}  # Сохраняем выбранный язык временно
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                          text='Отлично! Напишите свое имя.' if language == 'ru' else 'Ajoyib! Ismingizni yozing.')
    bot.register_next_step_handler(call.message, get_name)


# Получение имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправь свой номер!',
                     reply_markup=buttons.num_button())  # Используем кнопку для отправки контакта
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)


# Получение номера
def get_num(message, user_name):
    user_id = message.from_user.id

    # Если пользователь отправил контакт
    if message.contact:
        user_num = message.contact.phone_number
        # Заносим пользователя в БД
        baza.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    # Если пользователь написал номер в виде текста
    elif message.text:
        # Проверяем, является ли текст похожим на телефонный номер
        user_num = message.text
        if user_num.isdigit() and len(user_num) >= 10:  # Простейшая проверка на формат телефона
            # Заносим пользователя в БД
            baza.register(user_id, user_name, user_num)
            bot.send_message(user_id, 'Регистрация прошла успешно!',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            bot.send_message(user_id,
                             'Неверный формат номера! Пожалуйста, отправь свой номер через кнопку "Отправить контакт".')
            # Возврат на этап получения номера
            bot.register_next_step_handler(message, get_num, user_name)
    else:
        bot.send_message(user_id, 'Отправьте контакт по кнопке или отправьте номер через текстовое сообщение!')
        # Возврат на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)








# Запуск бота
bot.polling()