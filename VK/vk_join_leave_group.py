import csv
import time
from time import sleep

import requests

# Вступление или выход в\из сообщества VK

# для использования другими - приложение должно быть запущено!
# https://oauth.vk.com/authorize?client_id=******&display=page&scope=groups&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
token = ''
file_time = time.strftime('_%m-%d %H-%M-%S')

# Получение списка групп. Столбиком с дефисом: -1234567
with open('vk_join_leave_group.txt', 'r') as g_file:
    group = g_file.read().splitlines()


def let_join(group):
    counter = 1
    with open('vk_join_leave_group' + f'{file_time}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        try:
            for g in group:
                sleep(0.5)
                resp = requests.get('https://api.vk.com/method/groups.join'
                                    f'?group_id={g}'  # ID group
                                    f'&access_token={token}&v=5.131').json()
                print(resp)
                writer.writerow([g])
                print(g)
                counter += 1
                if 'error' in resp:
                    if resp.get('error').get('error_code') == 15:
                        print(f'Уже в группе. Группа: {g}')
                        writer.writerow([g, resp['error']['error_code']])
                if 'error' in resp:
                    if resp.get('error').get('error_code') == 14:
                        print(f'Ахтунг! капча: {g}')
                        print(resp)
                        writer.writerow([g, resp['error']['error_code']])
                        exit()
                if counter >= 15:
                    print('Спим 65 сек')
                    sleep(65)
                    print('Продолжаем :)')
                    counter = 1

        except KeyError:
            writer.writerow([g, 'KeyError'])
            print(f'Ошибка с id: {g}')
            pass
        except Exception as e:
            writer.writerow([g, 'Неизвестная ошибка'])
            print(e)
            pass


def let_leave(group):
    with open('vk_join_leave_group.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        try:
            for g in group:
                sleep(0.5)
                resp = requests.get('https://api.vk.com/method/groups.leave'
                                    f'?group_id={g}'
                                    f'&access_token={token}&v=5.131').json()
                # print(resp)
                if 'error' in resp:
                    if resp.get('error').get('error_code') == 15:
                        print(f'Уже в группе. Группа: {g}')
                        writer.writerow([g, resp['error']['error_code']])
        except KeyError:
            writer.writerow([g, 'KeyError'])
            print(f'Ошибка с id: {g}')
            pass
        except Exception as e:
            writer.writerow([g, 'Неизвестная ошибка'])
            print(e)
            pass


def handle_vkapi_captcha():
    captcha_sid = '763771919592'
    captcha_key = 'dedv'
    resp = requests.get('https://api.vk.com/method/groups.join'
                        f'?group_id={1}'  # ID group
                        f'&captcha_sid={captcha_sid}'
                        f'&captcha_key={captcha_key}'
                        f'&access_token={token}&v=5.131').json()
    print(resp)


start_time = time.time()
let_join(group)
# let_leave(group)
# handle_vkapi_captcha()
print("--- %s минут ---" % ((time.time() - start_time) / 60))
