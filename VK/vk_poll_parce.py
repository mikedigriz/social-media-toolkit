import csv
import time

import requests

# Сбор статы по голосованиям VK

# https://oauth.vk.com/authorize?client_id=******&scope=wall,groups&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
token = ''

file_time = time.strftime('_%m-%d %H:%M:%S')
# id сообщества -******
owner_id = '-*****'
# id опроса
poll_id = '******'
# id ответа
answer_ids = '******'
# сдвиг участников
offset = 0
# количество возвращаемых идентификаторов пользователей
count = 1000
# перечисленные через запятую поля анкет
voters_fields = 'nickname, screen_name, sex, bdate, city, country'


def get_poll_answers():
    with open('Варианты ответов и кол-во' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Варианты ответов', 'Голосов', 'ID'])

        resp = requests.get('https://api.vk.com/method/polls.getById'
                            f'?poll_id={poll_id}'  # ID group
                            f'&owner_id={owner_id}'
                            f'&access_token={token}&v=5.131').json()

        for _ in resp['response']['answers']:
            print(_['text'])
            print('Голосов:', _['votes'])
            print('ID:', _['id'])
            writer.writerow([_['text'], _['votes'], _['id']])


def get_poll_voters():
    resp = requests.get('https://api.vk.com/method/polls.getVoters'
                        f'?poll_id={poll_id}'  # ID group
                        f'&owner_id={owner_id}'
                        f'&answer_ids={answer_ids}'
                        f'&offset={offset}'
                        f'&count={count}'
                        f'&fields={voters_fields}'
                        f'&access_token={token}&v=5.131').json()

    with open('Участники голосования' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Имя', 'ID', 'День рождения', 'Город', 'Страна', 'Закрыта'])

        try:
            for _ in resp['response'][0]['users']['items']:
                if _.get('city'):
                    city = _['city']['title']
                else:
                    city = ''
                if _.get('country'):
                    country = _['country']['title']
                else:
                    country = ''
                writer.writerow(
                    [_.get('first_name') + ' ' + _.get('last_name'), f'https://vk.com/id' + str(_.get('id')),
                     _.get('bdate'), city, country, _.get('is_closed')])

        except Exception as e:
            print(e)
            pass


# get_poll_answers()
get_poll_voters()
