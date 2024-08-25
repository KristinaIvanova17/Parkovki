# Импорт импользуемых библиотек
from telebot import types
import telebot
import json

# Импорт модулей
from utils.check_location import check_loc
from utils.check_adress import check_adr

# Токен TELEGRAM ~ BotFather
bot = telebot.TeleBot('5982987139:AAF6IJ3Ann7X-ANjG9d9e4OfRc4HW6jHbFE')


# Регистрация пользователя
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    with open('./data/users.json', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

    str_id = str(message.from_user.id)

    if not str_id in data.keys():
        data[str_id] = {'first_name': message.from_user.first_name,
                        'select_city': '', 'action': 'choice_city'}
        bot.reply_to(message, 'Welcome to App Starter!')
        print(f'~~ Новый пользователь - {message.from_user.first_name}')

    with open("./data/users.json", "w", encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)
        jsonfile.close()

    return update(message)

# Обновление состояния пользователя action = [choice_city, choice_actions, check_adress, check_geolocation, read_adress, read_geolocation]
def update(message):
    with open('./data/users.json', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

    str_id = str(message.from_user.id)


    if str_id in data.keys():
        # choice_city
        if data[str_id]['action'] == 'choice_city':
            markup = types.ReplyKeyboardMarkup(
                row_width=1, input_field_placeholder='Выберите город:', resize_keyboard=True)
            item_btn1 = types.KeyboardButton('Санкт-Петербург')
            item_btn2 = types.KeyboardButton('Москва')
            markup.add(item_btn1, item_btn2)
            bot.send_message(message.chat.id, "Выберите город:",
                             reply_markup=markup)

        # choice_actions
        if data[str_id]['action'] == 'choice_actions' and data[str_id]['select_city'] != '':
            markup = types.ReplyKeyboardMarkup(
                row_width=1, input_field_placeholder='Выберите действие:', resize_keyboard=True)
            item_btn1 = types.KeyboardButton('Проверить адрес')
            item_btn2 = types.KeyboardButton('Проверить по геолокации')
            item_btn3 = types.KeyboardButton('Выбрать город')
            markup.add(item_btn1, item_btn2, item_btn3)
            bot.send_message(message.chat.id, "Выберите действие:",
                             reply_markup=markup)

        # check_adress
        if data[str_id]['action'] == 'check_adress' and data[str_id]['select_city'] != '':
            markup = types.ReplyKeyboardMarkup(
                row_width=1, input_field_placeholder='Напишите адрес', resize_keyboard=True)
            item_btn1 = types.KeyboardButton('Назад')
            markup.add(item_btn1)
            bot.send_message(message.chat.id, "Напишите адрес",
                             reply_markup=markup)

        # check_geolocation
        if data[str_id]['action'] == 'check_geolocation' and data[str_id]['select_city'] != '':
            markup = types.ReplyKeyboardMarkup(
                row_width=1, input_field_placeholder='Отправьте геоточку', resize_keyboard=True)
            item_btn1 = types.KeyboardButton('Назад')
            markup.add(item_btn1)
            bot.send_message(message.chat.id, "Отправьте геоточку",
                             reply_markup=markup)
        # read_adress
        if data[str_id]['action'] == 'read_adress' and data[str_id]['select_city'] != '':
            markup = types.ReplyKeyboardMarkup(
                row_width=1, input_field_placeholder=f'{data[str_id]["select_city"]} - Введите адрес', resize_keyboard=True)
            item_btn1 = types.KeyboardButton('Назад')
            markup.add(item_btn1)
            bot.send_message(message.chat.id, "Введите адрес",
                             reply_markup=markup)

        # read_geolocation
        if data[str_id]['action'] == 'read_geolocation' and data[str_id]['select_city'] != '':
            markup = types.ReplyKeyboardMarkup(
                row_width=1, input_field_placeholder=f'{data[str_id]["select_city"]} - Отправьте геоточку', resize_keyboard=True)
            item_btn1 = types.KeyboardButton('Назад')
            markup.add(item_btn1)
            bot.send_message(message.chat.id, "Отправьте геоточку",
                             reply_markup=markup)
    else:
        return handle_start(message)


# Обработчик кнопок + обработчик действий
@bot.message_handler(content_types=['text', 'location'])
def listen_chat(message):
    with open('./data/users.json', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

    str_id = str(message.from_user.id)
    if str_id in data.keys():

        # choice_actions
        if message.text in ['Санкт-Петербург', 'Москва'] and data[str_id]['select_city'] == '':
            with open('./data/users.json', "r", encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                jsonfile.close()

            str_id = str(message.from_user.id)

            data[str_id]['action'] = 'choice_actions'
            data[str_id]['select_city'] = message.text

            with open("./data/users.json", "w", encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False)
                jsonfile.close()

            return update(message)

        # Кнопка Назад
        if message.text == 'Назад':
            with open('./data/users.json', "r", encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                jsonfile.close()

            str_id = str(message.from_user.id)
            data[str_id]['action'] = 'choice_actions'

            with open("./data/users.json", "w", encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False)
                jsonfile.close()

            return update(message)

        # choice_city
        if message.text == 'Выбрать город':
            with open('./data/users.json', "r", encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                jsonfile.close()

            str_id = str(message.from_user.id)
            data[str_id]['action'] = 'choice_city'
            data[str_id]['select_city'] = ''

            with open("./data/users.json", "w", encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False)
                jsonfile.close()

            return update(message)

        # read_adress
        if message.text == 'Проверить адрес':
            with open('./data/users.json', "r", encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                jsonfile.close()

            str_id = str(message.from_user.id)
            data[str_id]['action'] = 'read_adress'

            with open("./data/users.json", "w", encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False)
                jsonfile.close()

            return update(message)

        # read_geolocation
        if message.text == 'Проверить по геолокации':
            with open('./data/users.json', "r", encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                jsonfile.close()

            str_id = str(message.from_user.id)
            data[str_id]['action'] = 'read_geolocation'

            with open("./data/users.json", "w", encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False)
                jsonfile.close()

            return update(message)

        # Проверка по Адресу
        if message.content_type == 'text' and data[str_id]['action'] == 'read_adress' and message.text != 'Проверить адрес':
            check_adr(message)

        # Проверка по Геолокации
        if message.content_type == 'location' and data[str_id]['action'] == 'read_geolocation':
            check_loc(message)
    else:
        return handle_start(message)

# Функция запуска сервера
def main():
    try:
        print('~~ Сервер запускается!')
        bot.polling(none_stop=True, interval=0, timeout=25)
    except Exception as e:
        print(f'~~ Ошибка -- {e}')
        main()


# Инициализация скрипта
if __name__ == '__main__':
    main()
