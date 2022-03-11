import requests
import datetime
from settings import token



def get_VK_URL_user(owner_id):
    now = datetime.datetime.now()
    year_now = now.strftime("%Y")
    URL = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': owner_id,
        'access_token': token()[0],
        'v': '5.131',
        'fields': 'sex, bdate, city, country, home_town, relation'
    }
    resp = requests.get(URL, params=params)
    user_info = (resp.json()['response'][0])
    print(user_info)
    try:
        temp = []
        temp.append({'id': user_info['id'], 'first_name': user_info['first_name'],
                     'last_name': user_info['last_name'], 'sex': user_info['sex'],
                     'bdate': user_info['bdate'], 'city': user_info['city']['id'],
                     'year_old': (int(year_now) - int(user_info['bdate'][-4:]))})
    except KeyError:
        temp = []
        temp.append({'id': user_info['id'], 'first_name': user_info['first_name'],
                     'last_name': user_info['last_name'], 'sex': user_info['sex'],
                     'bdate': None, 'city': None,
                     'year_old': 50})
    except ValueError:
        temp = []
        temp.append({'id': user_info['id'], 'first_name': user_info['first_name'],
                     'last_name': user_info['last_name'], 'sex': user_info['sex'],
                     'bdate': user_info['bdate'], 'city': user_info['city']['id'],
                     'year_old': None})
    return temp
