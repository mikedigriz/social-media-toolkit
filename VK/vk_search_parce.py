import csv
import time
from time import sleep

import requests

# Выполняет поиск сообществ по ключевым словам, заносит их в соответствующие файлики.
# Один из предварительных этапов для массового распространения тематической публикации в VK.

# Генерация токена
# https://oauth.vk.com/authorize?client_id=*******&scope=wall&response_type=token&v=5.131
# client_id это id приложения VK
token = ''

keyword_list = ['Велоспорт', 'Россия']
keyword_list_length = len(keyword_list)
start_time = time.time()


def vk_group_search(index_counter=1):
    for keyword in keyword_list:
        sleep(2)
        print(f"Выполняем поиск по {keyword} {index_counter}/{keyword_list_length}")
        index_counter += 1
        # Получаем список ID сообществ, удовлетворяющих ключевому слову
        resp_search = requests.get('https://api.vk.com/method/groups.search'
                                   f'?q={keyword}'
                                   '&sort=0'
                                   '&count=1000'
                                   f'&access_token={token}&v=5.131').json()

        group_ids = [g['id'] for g in resp_search['response']['items']]
        group_ids_1 = str(group_ids[:500]).strip('[]').replace(", ", ",")
        group_ids_2 = str(group_ids[500:]).strip('[]').replace(", ", ",")

        # Получаем список сообществ и разбиваем по 500 из-за ограничений метода groups.getById
        try:
            resp_detail1 = requests.get('https://api.vk.com/method/groups.getById'
                                        f'?fields=members_count,wall,can_message'
                                        f'&group_ids={group_ids_1}'
                                        f'&access_token={token}&v=5.131').json()
            sleep(1)
            resp_detail2 = requests.get('https://api.vk.com/method/groups.getById'
                                        f'?fields=members_count,wall,can_message'
                                        f'&group_ids={group_ids_2}'
                                        f'&access_token={token}&v=5.131').json()
        except IndexError:
            pass

        # Создаём csv-файл с сообществами 'ключевое_слово.csv'
        filename = keyword + ".csv"
        f = open(filename, 'w', newline='', encoding='utf8')
        writer = csv.writer(f)
        writer.writerow(['ID', 'Ссылка', 'Название сообщества', 'Подписчиков', 'Тип',
                         'Приватное сообщество(1-да)', 'Стенка(0-выкл,1-вкл,2-ограничена,3-закрыта)', 'Личка(1-да)'])

        try:
            for _ in resp_detail1['response']:
                # Проверка на блокировку сообщества
                if 'DELETED' in _['name']:
                    del _
                    print('Сообщество заблокировано!')
                    continue

                if _.__len__() != 9:
                    writer.writerow([_['id'], 'https://vk.com/' + _['screen_name'], _['name'],
                                     _['members_count'], _['type'],
                                     _['is_closed'], _['wall'],
                                     _['can_message']])
                else:
                    pass
        except KeyError as ke1:
            print(f'Тут ошибка KeyError_1, {ke1}')
            writer.writerow([f'Тут ошибка KeyError_1, {ke1}'])
            pass
        except Exception as ex1:
            print(ex1)
            writer.writerow([f'Неизвестная ошибка {ex1}'])
            pass
        try:
            for _ in resp_detail2['response']:
                if 'DELETED' in _['name']:
                    del _
                    print('Удаленная стр!')
                    continue

                if _.__len__() != 9:
                    writer.writerow([_['id'], 'https://vk.com/' + _['screen_name'], _['name'],
                                     _['members_count'], _['type'],
                                     _['is_closed'], _['wall'],
                                     _['can_message']])
                else:
                    pass
        except KeyError as ke2:
            print(f'Тут ошибка KeyError_2, {ke2}')
            writer.writerow([f'Тут ошибка KeyError_2, {ke2}'])
            pass
        except Exception as ex2:
            print(ex2)
            writer.writerow([f'Неизвестная ошибка {ex2}'])
            pass


# запуск
vk_group_search()
print("--- %s минут ---" % ((time.time() - start_time) / 60))
