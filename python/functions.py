from user import get_VK_URL_user
from find_users import filter_id
from db import select_count_id


def function(id):
    temp = select_count_id(id)
    if temp == [[]]:
        counter = 0
    else:
        counter = temp[0][0][1]
    user_info = get_VK_URL_user(id)
    city = user_info[0]['city']
    year_old = user_info[0]['year_old']
    sex = user_info[0]['sex']
    result = filter_id(city, year_old, sex, counter)
    if result == [] or result == [[]]:
        while result == [] or result == [[]]:
            counter = counter + 1
            result = filter_id(city, year_old, sex, counter)
    a = ((result[0][0]['id_profile']))
    b = {a}
    if set(temp[1:]) & b != set():
        while set(temp[1:]) & b != set():
            counter = counter + 1
            result = filter_id(city, year_old, sex, counter)
            if result == [] or result == [[]]:
                pass
            else:
                a = ((result[0][0]['id_profile']))
                b = {a}
    return result