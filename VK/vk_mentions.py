import csv
import time
from time import sleep

import requests

# Собирает упоминанния профиля

# для использования другими - приложение должно быть запущено!
# https://oauth.vk.com/authorize?client_id=******&scope=wall&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
token = ''
file_time = time.strftime('_%m-%d %H:%M:%S')
owner_id = [12345, 6789]
offset = 0
count = 50


def vk_get_mentions():
    start_time = time.time()
    with open('Упоминания акка' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'URL', 'Содержание'])
        sleep(0.5)
        for owner in owner_id:
            resp = requests.get('https://api.vk.com/method/newsfeed.getMentions'
                                f'?owner_id={owner}'
                                f'&offset={offset}'
                                f'&count={count}'
                                f'&access_token={token}&v=5.131').json()
            # print(resp)
            if 'response' in resp:
                for _ in resp['response']['items']:
                    if _['post_type'] == 'reply':
                        if not _['parents_stack']:
                            print(_['text'])
                            main_id = _['id']
                            to_id = _['to_id']
                            post_id = _['post_id']
                            print('URL:', f'https://vk.com/wall{from_id}_{id_post}')
                            writer.writerow([owner, f'https://vk.com/wall{to_id}_{post_id}?reply={main_id}', _['text']])
                        else:
                            parents_stack = _['parents_stack'][0]
                            print(_['text'])
                            main_id = _['id']
                            to_id = _['to_id']
                            post_id = _['post_id']
                            print('URL:', f'https://vk.com/wall{from_id}_{id_post}')
                            writer.writerow(
                                [owner, f'https://vk.com/wall{to_id}_{post_id}?reply={main_id}&thread={parents_stack}',
                                 _['text']])
                    if _['post_type'] == 'post':
                        print(_['text'])
                        from_id = _['from_id']
                        id_post = _['id']
                        print('URL:', f'https://vk.com/wall{from_id}_{id_post}')
                        writer.writerow([owner, f'https://vk.com/wall{from_id}_{id_post}', _['text']])
        print("--- %s минут ---" % ((time.time() - start_time) / 60))


vk_get_mentions()
