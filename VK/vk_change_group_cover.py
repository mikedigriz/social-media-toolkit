import json

import requests

# Меняет обложку в сообществе
# TODO Сделать слайдшоу или динамическую смену обложек с добавлением разных данных статистики

# Как получить access_token:
# https://oauth.vk.com/authorize?client_id=*****&scope=photos&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.

token = ''
group_id = ''


def upload_img():
    upload_cover = requests.get('https://api.vk.com/method/photos.getOwnerCoverPhotoUploadServer'
                                f'?group_id={int(group_id)}'
                                f'&crop_x=0&crop_y=0&crop_x2=1920&crop_y2=265'
                                f'&access_token={token}&v=5.131').json()

    upload_url = upload_cover['response']['upload_url']
    send_banner = requests.post(upload_url, files={'photo': open('vk_profile_banner.jpg', "rb")})
    hash_and_photo = json.loads(send_banner.text)
    hash_img = hash_and_photo['hash']
    photo = hash_and_photo['photo']
    save_cover = requests.post('https://api.vk.com/method/photos.saveOwnerCoverPhoto'
                               f'?access_token={token}&v=5.131'
                               f'&hash={hash_img}'
                               f'&photo={photo}')
    print(save_cover)


upload_img()
