import csv
import time
from time import sleep

import vk

# TODO Заменить либу на requests

# Как получить access_token:
# https://oauth.vk.com/authorize?client_id=*****&display=page&scope=friends&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
access_token = ''
v = '5.131'
file_time = time.strftime('_%m-%d %H-%M-%S')

# Подключение к VK API
session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)

user_list = [
    '25552703',
    '25552704',
    '25552705',
    '25552706',
    '25552707'
]


def vk_count_user_followers():
    with open('vk_count_user_followers' + f'{file_time}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for user in user_list:
            sleep(0.4)
            try:
                vk_users = api.friends.get(user_id=user, count=999999)
                print(user, vk_users['count'])
                writer.writerow([user, vk_users['count']])
            except vk.exceptions.VkAPIError:
                print(f'Проблема с id: {user}')
                writer.writerow([user, ''])
                continue


start_time = time.time()
vk_count_user_followers()
print("--- %s минут ---" % ((time.time() - start_time) / 60))
