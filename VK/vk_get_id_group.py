import csv
import time
from time import sleep

import requests

# для использования другими - приложение должно быть запущено!
# https://oauth.vk.com/authorize?client_id=******&display=page&scope=wall&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
token = ''
file_time = time.strftime('_%m-%d %H-%M-%S')

# Получение списка групп. Столбиком с дефисом: -1234567
with open('vk_get_id_group' + f'.txt', 'r') as g_file:
    group = g_file.read().splitlines()


def get_group_id(group):
    with open('vk_group_id' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID'])
        for g in group:
            sleep(0.5)
            resp = requests.get('https://api.vk.com/method/groups.getById'
                                f'?group_ids={g}'  # ID group
                                f'&fields='  # опциональное поле
                                f'&access_token={token}&v=5.131').json()  # token
            try:
                for _ in resp:
                    writer.writerow([resp['response'][0]['id']])
            except KeyError:
                writer.writerow([g, 'Ошибка', 'Ошибка', 'Ошибка', 'Ошибка', 'Ошибка'])
                print(f'Ошибка с id: {g}')
                pass
            except Exception as e:
                print(e)
                print(resp['response'][0]['id'], 'тут что-то сломано...')
                writer.writerow([g, 'Неизвестная ошибка', 'Неизвестная ошибка'])
                pass


start_time = time.time()
get_group_id(group)
print("--- %s минут ---" % ((time.time() - start_time) / 60))
