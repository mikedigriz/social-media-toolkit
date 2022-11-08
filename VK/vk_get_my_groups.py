import csv
import time

import requests

# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
# https://oauth.vk.com/authorize?client_id=*****&display=page&response_type=token
token = ''

file_time = time.strftime('_%m-%d %H:%M:%S')
# id человека
user_id = 25552703
# доп.поля
extended = 1
# сдвиг
offset = 0
# количество возвращаемых идентификаторов пользователей
count = 1000


def get_followed_group():
    with open('Группы в подписках' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Имя', 'Тип'])

        resp = requests.get('https://api.vk.com/method/groups.get'
                            f'?user_id={user_id}'  # ID group
                            f'&extended={extended}'
                            f'&count={count}'
                            f'&access_token={token}&v=5.131').json()
        # print(resp)
        for _ in resp['response']['items']:
            print('ID:', _['id'])
            print('Имя:', _['name'])
            print('Тип:', _['type'])
            writer.writerow([_['id'], _['name'], _['type']])


get_followed_group()
