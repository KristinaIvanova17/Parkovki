from dadata import Dadata
import telebot
import json

bot = telebot.TeleBot('5982987139:AAF6IJ3Ann7X-ANjG9d9e4OfRc4HW6jHbFE')

token = "8b1ae26c7efee102621070e4cd1241069ad4612a"
secret = "7b970f91044a73b8d1a40a5184924a8ceaaf6d04"

# Проверка Геолокации
def check_loc(message):
    with open('./data/users.json', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

        str_id = str(message.from_user.id)

        dadata = Dadata(token, secret)
        result = dadata.geolocate(
            name="address", lat=message.json['location']['latitude'], lon=message.json['location']['longitude'], count=1)

        pr_result = result[0]['value']
        pr_region = result[0]['data']['region']
        pr_street = result[0]['data']['street']
        pr_litter = result[0]['data']['block'] if result[0]['data']['block'] != None else ''
        pr_house = result[0]['data']['house'] if result[0]['data']['house'] != None else '' + pr_litter

        if pr_region != data[str_id]['select_city'] or pr_street == None:
            print(f"~~ {data[str_id]['first_name']} проверил гео ширина {message.json['location']['latitude']} долгота {message.json['location']['longitude']} - Неверный адрес")
            return bot.reply_to(
                message, f"<b>{data[str_id]['select_city']}</b>\n <i>-Адрес не найден</i>", parse_mode="HTML")
            

        with open('./data/parking_data.json', encoding='utf-8') as jsonfile:
            parking_data = json.load(jsonfile)
            jsonfile.close()

        all_free_parking = 0
        all_paid_parking = 0
        all_parkomat = 0

        flag_template_paid = False
        flag_template_free = False
        flat_template_parkomat = False

        for adress in parking_data[data[str_id]['select_city']]:
            if adress['street'] == pr_street:
                for list_parking in adress['parking']:
                    if "paid_parking" in list_parking:
                        all_paid_parking += 1
                    if "free_parking" in list_parking:
                        all_free_parking += 1
                    if "parkomat" in list_parking:
                        all_parkomat += 1
                if adress['house'] == pr_house:
                    if "paid_parking" in list_parking:
                        flag_template_paid = True
                        info_paid_parking_zone = list_parking['paid_parking']['zone']
                        info_paid_parking_places = list_parking['paid_parking']['places']
                        info_paid_parking_A_auto = list_parking['paid_parking']['A_auto']
                        info_paid_parking_B_auto = list_parking['paid_parking']['B_auto']
                        info_paid_parking_C_auto = list_parking['paid_parking']['C_auto']
                        info_paid_parking_D_auto = list_parking['paid_parking']['D_auto']
                    if "free_parking" in list_parking:
                        flag_template_free = True
                        info_free_parking_zone = list_parking['free_parking']['zone']
                        info_free_parking_places = list_parking['free_parking']['places']
                    if "parkomat" in list_parking:
                        flat_template_parkomat = True
                        info_parkomat_zone = list_parking['parkomat']['zone']

        temlate_count_parking = f"   Платные парковки: <b>{all_paid_parking}</b>\n   Бесплатные парковки: <b>{all_free_parking}</b>\n   Паркоматы: <b>{all_parkomat}</b>\n"

        if flag_template_paid:
            template_paid_parking = f"<i>Платная парковка</i>\n   Зона: <b>#{info_paid_parking_zone}</b>\n   Места: <b>{info_paid_parking_places}</b>\n   Мотоцикл:           <b>{info_paid_parking_A_auto}</b> руб. в час\n   Легковой авто:  <b>{info_paid_parking_B_auto}</b> руб. в час\n   Грузовой авто:  <b>{info_paid_parking_C_auto}</b> руб. в час\n   Микроавтобус:  <b>{info_paid_parking_D_auto}</b> руб. в час\n"
        else:
            template_paid_parking = ""

        if flag_template_free:
            template_free_parking = f"<i>Бесплатная парковка</i>\n   Зона: <b>#{info_free_parking_zone}</b>\n   Места: <b>{info_free_parking_places}</b>\n"
        else:
            template_free_parking = ""

        if flat_template_parkomat:
            template_parkomat_parking = f"<i>Паркомат</i>\n   Зона: <b>#{info_parkomat_zone}</b>"
        else:
            template_parkomat_parking = ""

        bot.reply_to(
            message, f"<b>{pr_result}</b>\n<i>Информация о парковках:</i>\n{temlate_count_parking}\n{template_paid_parking}{template_free_parking}{template_parkomat_parking}", parse_mode="HTML")
        print(f"~~ {data[str_id]['first_name']} проверил гео ширина {message.json['location']['latitude']} долгота {message.json['location']['longitude']} - Верный адрес")
