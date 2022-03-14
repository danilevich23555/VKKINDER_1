import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from functions import function, function_no_param
from user import get_VK_URL_user
from db import write_db, select_count_id_no_city, write_db_user_nocity
from settings import token
from create_db_or_no import create_db_write_txt
import datetime
import json
from city import get_country, get_city


create_db_write_txt()


vk = vk_api.VkApi(token=token()[0])
longpoll = VkLongPoll(vk)
counter = 0
flag = 0

json1 = {
    "one_time": False,
    "buttons": [
        [
           {
               "action": {
                   "type": "text",
                   "payload": "{\"command\":\"start\", \"button\": \"1\"}",
                   "label": "Правила использывания бота"
               },
               "color": "secondary"
           }
        ],
        [
           {
               "action": {
                   "type": "text",
                   "payload": "{\"button\": \"2\"}",
                   "label": "Подобрать пару"
               },
               "color": "secondary"
           }
        ]
    ]
   }
print(json1)
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': 0, 'keyboard': json.dumps(json1)})
def write_msg1(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': 0, 'keyboard': json.dumps(keyboard)})



print('Приложение запущено')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "Подобрать пару" or request == "привет":
                counter = counter + 1
                result_user = get_VK_URL_user(event.user_id)
                if result_user[0]['city'] == None:
                    if select_count_id_no_city(event.user_id) == [[]]:
                        keybord_country = get_country()
                        write_msg1(event.user_id, 'Для подбора пары необходимо указать Страну, введите с клавиатуры вашу страну!', keybord_country[0])
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    request_country = event.text
                                    key_city = get_city(request_country, keybord_country[1])
                                    write_msg1(event.user_id,
                                               'Для подбора пары необходимо указать город, введите с клавиатуры ваш город!',
                                               key_city[0])
                                    for event in longpoll.listen():
                                        if event.type == VkEventType.MESSAGE_NEW:
                                            if event.to_me:
                                                request_city = event.text
                                                flag = flag + 1
                                                for city_id in range(len(key_city[1])):
                                                    if key_city[1][city_id]['title'] == request_city:
                                                        id_city = int(key_city[1][city_id]['id'])
                                                        break
                                                write_msg(event.user_id,
                                                          'Для побора пары необходим Ваш год рождения, '
                                                          'напишите боту его(пример 1991).',
                                                          )
                                                for event in longpoll.listen():
                                                    if event.type == VkEventType.MESSAGE_NEW:
                                                        if event.to_me:
                                                            request_year_old = event.text
                                                            write_db_user_nocity(event.user_id, id_city, request_city, request_year_old)
                                                            break
                                                break
                                    break
                    else:
                        flag = flag + 1
                        id_city = select_count_id_no_city(event.user_id)[0][0][1]
                        request_year_old = select_count_id_no_city(event.user_id)[0][0][3]
                if flag == 1:
                    flag = 0
                    result = function_no_param(event.user_id, id_city, request_year_old)
                else:
                    result = function(event.user_id)
                for line in range(len(result)):
                    if len(result[line]) == 2:
                        write_db(event.user_id, result[line][0]['id_profile'], result[line][0]['url_profile'],
                                 result[line][0]['url_photo'], result[line][1]['url_photo'],
                                 None)
                        write_msg(event.user_id, f"Профайл: \n {result[line][0]['url_profile']} \n Фото: "
                                                 f"\n {result[line][0]['url_photo']}, \n {result[line][1]['url_photo']}"
                                  )
                        now = datetime.datetime.now()
                        print(f'-------------------------------{counter}----------------------------------')
                        print(
                            f'{now.strftime("%d-%m-%Y-%H-%M-%S")} для ID: {event.user_id} найдена пара с ID: '
                            f'{result[line][0]["id_profile"]}\n'
                            f'найденные данные занесы в БД\n'
                            f'-----------------------------------------------------------------')
                    elif len(result[line]) == 1:
                        write_db(event.user_id, result[line][0]['id_profile'], result[line][0]['url_profile'],
                                 result[line][0]['url_photo'], None, None)
                        write_msg(event.user_id, f"Профайл: \n {result[line][0]['url_profile']} \n Фото: "
                                                 f"\n {result[line][0]['url_photo']}")
                        now = datetime.datetime.now()
                        print(f'-------------------------------{counter}----------------------------------')
                        print(
                            f'{now.strftime("%d-%m-%Y-%H-%M-%S")} для ID: {event.user_id} найдена пара с ID: '
                            f'{result[line][0]["id_profile"]}\n'
                            f'найденные данные занесы в БД\n'
                            f'---------------------------------------------------------------')
                    elif len(result[line]) == 0:
                        pass
                    else:
                        write_db(event.user_id, result[line][1]['id_profile'], result[line][1]['url_profile'],
                                 result[line][0]['url_photo'], result[line][1]['url_photo'],
                                 result[line][2]['url_photo'])
                        write_msg(event.user_id, f"Профайл: \n {result[line][0]['url_profile']} \n Фото: "
                                                 f"\n {result[line][0]['url_photo']}, \n "
                                                 f"{result[line][1]['url_photo']},"
                                                 f"\n " f"{result[line][2]['url_photo']}")
                        now = datetime.datetime.now()
                        print(f'-------------------------------{counter}----------------------------------')
                        print(f'{now.strftime("%d-%m-%Y-%H-%M-%S")} для ID: {event.user_id} найдена пара с ID: '
                              f'{result[line][0]["id_profile"]}\n'f'найденные данные занесы в БД\n'
                              f'-----------------------------------------------------------------')
            elif request == "Правила использывания бота":
                write_msg(event.user_id,
                          '- необходимо написать слово "привет" или нажать кнопку "подобрать пару" в сообщество в VK,\n'
                          'куда через некоторое время придут ссылки на профиль и фотографии подходящего вам человека \n'
                          'по городу и возрасту(+\- 5 лет).\n'
                          '- для запроса по подбору новой пары необходимо повторно написать слово "привет" или нажать\n'
                          'кнопку "подобрать пару" в сообщество VK.\n'
                          '- при каждом новом запросе приходет ссылка на новую пару.')
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")