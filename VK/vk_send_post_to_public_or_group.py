import csv
import time
from datetime import datetime
from time import sleep

import requests

from utils import utils

# Инструмент для массового распостранения публикаций в сообществах VK.

# TODO: задеплоить автоматическую смену токена по достижению лимита без остановки работы

# Для использования своего приложения другими аккаунтами - оно должно быть запущено, а токен сгенерен из одной сети!
# Открыть с аккаунта для раскидки
# https://oauth.vk.com/authorize?client_id=********&scope=wall,groups&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
token = ''

# Получение списка групп. Столбиком с дефисом: -1234567
with open('vk_send_post_group.txt', 'r') as g_file:
    group = g_file.read().splitlines()
# Получение списка Блэклист. Столбиком с дефисом: -1234567
with open('blacklist_group.txt', 'r') as g_file:
    blacklist = g_file.read().splitlines()
# Ссылка на видео
video = 'video-97585145_456239026'

# Текст поста. Используй urlencode для хештегов и.т.п.
post_text = 'Явное лучше, чем неявное 💪🏻\n\n' \
            'Простое лучше, чем сложное...\n\n' \
            '%23python %23programming'

file_time = time.strftime('_%m-%d %H-%M-%S')


def is_blacklisted(group, blacklist):
    """Мы не хотим раскидывать в эти сообщества публикацию ни при каких условиях"""
    send_list = []
    for i in group:
        if i not in blacklist:
            send_list.append(i)
        else:
            print(f'Опа, группа из блэклиста: {i}')
            pass
    return send_list


def vk_send_post(group, blacklist, post_text, video, token):
    """Отправляет пост(текст, фото или видео) в сообщества из списка vk_send_post_group.txt
       Ограничения VK: 100 постов на аккаунт, 2 поста в секунду
       Учитывается блэклист.
       Если сообщество закрыто для акка или требует вступить - пропускаем."""

    send_count = 0
    start_time = time.time()

    # переназначение проверенного списка в кач-ве основного
    group = is_blacklisted(group, blacklist)
    print(f'Кол-во валидных id для публикации: {len(group)}')

    with open('Раскидка от' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Ссылки на публикации в паблики и группы VK'])
        try:
            for g in group:
                sleep(2)
                resp = requests.get('https://api.vk.com/method/wall.post'
                                    f'?owner_id={g}'  # ID group
                                    f'&attachments={video}'  # video
                                    '&from_group=0'
                                    f'&message={post_text}'
                                    f'&access_token={token}&v=5.131').json()
                if 'response' in resp:
                    post_link = resp['response']['post_id']
                    print(f'https://vk.com/wall{g}_{post_link}')
                    writer.writerow([f'https://vk.com/wall{g}_{post_link}'])
                    print(datetime.today().strftime(f'%H:%M:%S | Пост отправлен!\n'
                                                    f'Группа: {g}'))
                    print(datetime.today().strftime(f'%H:%M:%S | Отправлено постов: {send_count + 1}'))
                    send_count += 1

                if 'error' in resp:
                    if resp.get('error').get('error_code') == 214:
                        print(datetime.today().strftime(f'%H:%M:%S | Ошибка при отправке поста. Возможно ЧС.\n'
                                                        f'Группа: {g}'))
                        writer.writerow([f'https://vk.com/public{g[1:]}', 'Ошибка 214'])
                    if resp.get('error').get('error_code') == 15:
                        print(datetime.today().strftime(f'%H:%M:%S | Нет прав.\n'
                                                        f'Группа: {g}'))
                        writer.writerow([f'https://vk.com/public{g[1:]}', 'Ошибка 15'])
                    if resp.get('error').get('error_code') == 14:
                        print(datetime.today().strftime(f'%H:%M:%S | Каптча.\n'
                                                        f'Группа: {g}'))
                        writer.writerow([f'https://vk.com/public{g[1:]}', 'Каптча сработала'])
                        print(resp)
                        utils.beep()
                        print('Выход')
                        exit()
                    if resp.get('error').get('error_code') == 220:
                        print(datetime.today().strftime(f'%H:%M:%S | Лок аккаунта, завершаем.\n'
                                                        f'Группа: {g}'))
                        writer.writerow([f'https://vk.com/public{g[1:]}', 'Ошибка 220'])
                        utils.beep()
                        exit()
                    else:
                        print(datetime.today().strftime(f'%H:%M:%S | Произошла ошибка.'))
                        print(resp)
                        print(g, '- Последняя Группа')
                        writer.writerow([f'https://vk.com/public{g[1:]}', 'Пропуск'])
                        print('Пауза 1 сек.')
                        sleep(1)
        except Exception as err:
            print(datetime.today().strftime(f'%H:%M:%S | Произошла ошибка:\n {err}'))
        print("--- %s минут ---" % ((time.time() - start_time) / 60))
        utils.beep()


def handle_vkapi_captcha():
    """Если срабатывает капча, нужно вызвать функцию и передать параметры captcha_sid, captcha_key"""
    captcha_sid = '880502812978'
    captcha_key = 'zzhn'
    resp = requests.get('https://api.vk.com/method/groups.leave'
                        f'?group_id={1}'  # это формальность
                        f'&captcha_sid={captcha_sid}'
                        f'&captcha_key={captcha_key}'
                        f'&access_token={token}&v=5.131').json()
    print(resp)


if __name__ == '__main__':
    vk_send_post(group, blacklist, post_text, video, token)
    # handle_vkapi_captcha()
