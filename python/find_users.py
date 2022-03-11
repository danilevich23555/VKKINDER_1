import requests
import time
from settings import token





def get_VK_URL (city, year_old, sex, counter):
    URL = 'https://api.vk.com/method/users.search'
    if sex == 1:
        sex = 2
    else:
        sex = 1
    params = {
        'sort': 0,
        'city': city,
        'access_token': token()[1],
        'v': '5.131',
        'fields': 'sex, bdate, city, country, home_town, relation',
        'count': 1,
        'sex': sex,
        'age_from': int(year_old) - 5,
        'age_to': int(year_old) + 5,
        'status': 6,
        'offset': counter
        }
    resp = requests.get(URL, params=params)
    return resp




def get_VK_URL_foto_like(owner_id):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': owner_id,
        'album_id': 'profile',
        'extended': 1,
        'access_token': token()[1],
        'v': '5.131'
    }
    time.sleep(0.8)
    resp = requests.get(URL, params=params, timeout=50000)
    quntity_foto = (len((resp.json()['response']['items'])))
    temp = []
    for foto in range(quntity_foto):
        url_photo = (resp.json()['response']['items'][foto])['sizes'][-1]['url']
        like = (resp.json()['response']['items'][foto]['likes']['count'])
        url_profile = 'https://vk.com/id' + str(owner_id)
        id_profile = (owner_id)
        temp.append({'id_profile': id_profile,'url_profile': url_profile,'url_photo': url_photo, 'like': like})
    return temp



def filter_id(city, year_old, sex, counter):
    a = get_VK_URL(city, year_old, sex, counter).json()['response']['items']
    count_id = len(a)
    temp_id = []
    for i in range((count_id)):
        if a[i]['is_closed'] == False:
            temp_id.append(a[i]['id'])
        else:
            pass
    temp_result = []
    for i in range(len(temp_id)):
        result = get_VK_URL_foto_like(temp_id[i])
        sorted_result = sorted(result, key=lambda d: d['like'], reverse=True)
        temp_result.append(sorted_result[:3])
    return temp_result

