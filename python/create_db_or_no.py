import psycopg2
from pathlib import Path
import os


temp_param = []
path = os.path.join(Path(__file__).parents[1], 'connection_db')

def examination():
    with open(f"{path}\\connection_db.txt", 'r') as param:
        for string in param:
                temp_param.append(string.strip())
    con = psycopg2.connect(
        database=temp_param[0],
        user=temp_param[1],
        password=temp_param[2],
        host=temp_param[3],
        port=temp_param[4]
      )
    cur = con.cursor()
    postgres_insert_query = """SELECT EXISTS(SELECT 1 FROM information_schema.tables 
                  WHERE table_catalog='postgres' AND 
                        table_schema='public' AND 
                        table_name='vkkinder');"""
    cur.execute(postgres_insert_query)
    answer = cur.fetchall()
    return answer[0][0]

def create_db_write_txt():
    if int(os.stat(f"{path}\\connection_db.txt").st_size) == 0:
        print('Cейчас будет создана база даннык vkkinderdb postgresql для работы приложения VKKINDER, для этого\n'
              'заполните данные ниже: ')
        database = input('Введите имя схемы БД (postgres): ')
        user = input('Введите имя пользователя(postgres): ')
        password = input("Введите пароль: ")
        host = input("Введите адрес хоста(localhost): ")
        port = input("Введите номер порта(5432): ")
        with open(f"{path}\\connection_db.txt", 'w') as param:
            param.write(f"{database}\n")
            param.write(f"{user}\n")
            param.write(f"{password}\n")
            param.write(f"{host}\n")
            param.write(f"{port}")
    a = int(os.stat(f"{path}\\connection_db.txt").st_size)
    b = examination()
    if examination() == False:
        with open(f"{path}\\connection_db.txt", 'r') as param:
            for string in param:
                    temp_param.append(string.strip())
        con = psycopg2.connect(
            database=temp_param[0],
            user=temp_param[1],
            password=temp_param[2],
            host=temp_param[3],
            port=temp_param[4]
        )
        cur = con.cursor()
        postgres_insert_query = """create table if not EXISTS vkkinder (id_user integer, id_user_find integer, url_profile varchar(300), 
            url_foto_1 varchar(300), url_foto_2 varchar(300), url_foto_3 varchar(300));"""
        cur.execute(postgres_insert_query)
        con.commit()
        cur = con.cursor()
        postgres_insert_query = """create table if not EXISTS user_nocity_noyearold (id_user integer, id_city integer, 
        title varchar(300), yearold varchar(300));"""
        cur.execute(postgres_insert_query)
        con.commit()
        print('База данных создана.\n'
              'Правило использывания приложения: \n'
              '- необходимо написать слово "привет" в сообщество в VK, куда через некоторое время придут ссылки \n'
              'на профиль и фотографии подходящего вам человека по городу и возрасту(+\- 5 лет).\n'
              '- для запроса по подбору новой пары необходимо повторно написать слово "привет" в сообщество VK.\n'
              '- при каждом новом запросе приходет ссылка на новую пару.')
    return [a,b]


