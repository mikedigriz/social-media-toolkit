from time import sleep

import requests

# Рассылка сообщений в VK

# для использования другими - приложение должно быть запущено!
# https://oauth.vk.com/authorize?client_id=******&scope=messages&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
token = ''

# ID контактов, если личка группы - то начинается с '-123456789'
peer_id = ['23456789',
           '-321456'
           ]

# Прикрепляемая картинка
attachment = 'photo-******_152250651'

# Получение текста
message = 'Здравствуйте! Опубликуйте, пожалуйста ❤'


def vk_send_message(peer_id, message, token):
    send_count = 0
    for g in peer_id:
        try:
            sleep(0.5)
            resp = requests.get('https://api.vk.com/method/messages.send'
                                f'?peer_id={g}'
                                f'&message={message}'
                                f'&random_id=0'
                                f'&attachment={attachment}'
                                f'&access_token={token}&v=5.131').json()
            if 'response' in resp:
                send_count += 1
                print(f'Отправлено в {g}', f'Итого: {send_count}')
            else:
                print(f'Ответ не получен для {g}')
                print(resp)
        except Exception as ex:
            print(ex)
            break


def handle_vkapi_captcha():
    captcha_sid = '745474924595'
    captcha_key = 'dqyuh'
    resp = requests.get('https://api.vk.com/method/groups.join'
                        f'?group_id={1}'  # ID group
                        f'&captcha_sid={captcha_sid}'
                        f'&captcha_key={captcha_key}'
                        f'&access_token={token}&v=5.131').json()
    print(resp)


vk_send_message(peer_id, message, token)
