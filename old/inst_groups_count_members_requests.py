import csv
import random
import re
import time
from time import sleep

import requests

# Первый вариант подсчета числа подписчиков заданных страниц. Так как доступ к API легко не получить, используется requests.
# Не рекомендуется использовать из-за сильной возможности блокировки аккаунта или других ограничений.
# Существует варианты автоматизации с selenium,bs4 например реализация InstaPy. Но многие действия блочатся инстой со второго раза.

file_time = time.strftime('_%m-%d %H-%M-%S')

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive',
}

page_list = [
    'instagram_account_1',
    'instagram_account_2',
    'instagram_account_3'
]

with open('Стата_соц_сеток_inst_requests' + f'{file_time}.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for page in page_list:
        try:
            sleep(random.uniform(1, 3))
            url = 'https://www.instagram.com/' + page
            r = requests.get(url, headers=headers).text
            followers = re.search('"edge_followed_by":{"count":([0-9]+)}', r).group(1)
            print(f'{page} подписано: {followers}')
        except Exception as ex:
            print(ex)
            continue
        finally:
            writer.writerow([page, followers])
