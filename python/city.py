import requests
from settings import token
import  json




def get_country():
    URL = 'https://api.vk.com/method/database.getCountries'
    params = {
        'access_token': token()[1],
        'v': '5.131',
        'need_all': 0
    }
    resp = requests.get(URL, params=params)
    user_info = (resp.json())
    result_country = ((user_info['response']['items']))
    temp = []
    json_button_country = []
    json_keyboard = []
    counter = 0
    for country in range(len(result_country)):
        if country % 3 == 0:
            counter = counter + 1
            if country != 0:
                temp.append(json_button_country)
                json_button_country = []
        json_button_country.append({'action': {'type': 'text', 'payload': {'command': 'start', 'button': counter},
                                                'label': result_country[country]['title']}, 'color': 'secondary'})
    temp.append(json_button_country)
    json_keyboard.append({'one_time': True,'buttons': temp})

    return [json_keyboard[0], result_country]

print(get_country())
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
def get_city(country, dict_country):
    for country_id in range(len(dict_country)):
        if dict_country[country_id]['title'] == country:
            id_country = int(dict_country[country_id]['id'])
            break
    URL = 'https://api.vk.com/method/database.getCities'
    params = {
        'country_id': id_country,
        'access_token': token()[1],
        'v': '5.131',
        'need_all': 0

    }
    resp = requests.get(URL, params=params)
    user_info = (resp.json())
    result_city = ((user_info['response']['items']))
    temp = []
    json_button_country = []
    json_keyboard = []
    counter = 0
    for country in range(len(result_city)):
        if country % 4 == 0:
            counter = counter + 1
            if country != 0:
                temp.append(json_button_country)
                json_button_country = []
        json_button_country.append({'action': {'type': 'text', 'payload': {'command': 'start', 'button': counter},
                                               'label': result_city[country]['title']}, 'color': 'secondary'})
    temp.append(json_button_country)
    json_keyboard.append({'one_time': True, 'buttons': temp})

    return [json_keyboard[0], result_city]
