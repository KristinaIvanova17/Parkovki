import telebot
from dadata import Dadata

bot = telebot.TeleBot('5982987139:AAF6IJ3Ann7X-ANjG9d9e4OfRc4HW6jHbFE')
token = "8b1ae26c7efee102621070e4cd1241069ad4612a"
secret = "7b970f91044a73b8d1a40a5184924a8ceaaf6d04"


@bot.message_handler(content_types=['text'])
def check_adr(message):
    dadata = Dadata(token, secret)
    result = dadata.clean("address", message.text)

    print('Результат - ', result['result'])
    print('Город - ', result['region'])
    print('Улица - ', result['street'])
    print('Дом - ', result['house'])
    print('Буква - ', result['block'])
    print('################################')


# Функция запуска сервера
def main():
    bot.polling(none_stop=True, interval=0, timeout=25)


# Инициализация скрипта
if __name__ == '__main__':
    main()
