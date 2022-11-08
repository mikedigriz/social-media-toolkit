# TikTok version: 19.3.4
from time import sleep

import uiautomator2 as u2

# Автоматизация действий с подписчиками и друзьями TikTok
# TikTok под каждую новую версию меняет id элементов.
# Язык приложения имеет значение.

# USB - Connection
d = u2.connect('R58M31BXMNT')  # get from "adb devices"
# WiFi - Connection
# d = u2.connect('192.168.1.130:5555')
height = d.info.get('displayHeight')
width = d.info.get('displayWidth')
heightCenter = height / 2
widthCenter = width / 2
heightDown = height / 1.5
heightUp = height / 10


def start_app():
    d.app_start('com.zhiliaoapp.musically', stop=True, use_monkey=True)


def kill_app():
    d.app_stop('com.zhiliaoapp.musically')


def unfollow_non_followers():
    start_app()
    d(text="Я").click()
    # follows
    d(text='Подписки', className='android.widget.TextView').click()
    sleep(1)
    d.swipe_ext("up", scale=0.7, duration=0.1)
    follow = d(text='Подписки', className='android.widget.TextView')
    counter = 0
    kill_proc = 0
    while True:
        d.swipe_ext("up", scale=0.7, duration=0.1)
        sleep(0.8)
        if follow.exists() in range(0, 9):
            for _ in follow:
                kill_proc -= kill_proc
                follow.click()
                sleep(0.5)
                counter += 1
                print(f'Отписались от {counter} чел.')
        if not follow.exists():
            kill_proc += 1
            if kill_proc == 180:
                print('Элементы не найдены. Завершение работы программы')
                kill_app()
                exit()


def follow_followers():
    kill_proc = 0
    counter = 0
    start_app()
    d(text="Я").click()
    # followers
    d(text='Подписчики', className='android.widget.TextView').click()
    follow = d(text='Добавить в ответ', className='android.widget.TextView')
    while True:
        if follow.exists() in range(0, 9):
            kill_proc -= kill_proc
            for _ in follow:
                follow.click()
                sleep(0.7)
                counter += 1
                print(f'Добавлено ответно в друзья {counter} чел.')
            else:
                kill_proc += 1
                if kill_proc == 20:
                    print('Элементы не найдены. Завершение работы программы')
                    kill_app()
                    exit()
        d.swipe_ext("up", scale=0.7, duration=0.2)
        sleep(1)


def follow_new_guy():
    start_app()
    d(text="Я").click()
    d(text='Подписчики', className='android.widget.TextView').click()
    d(resourceId="android:id/text1", text="Рекомендуемые").click()
    counter = 0
    kill_proc = 0
    follow = d(text='Подписаться', className='android.widget.TextView')
    while True:
        sleep(1)
        if follow.exists() in range(0, 7):
            for _ in follow:
                kill_proc -= kill_proc
                follow.click()
                sleep(0.8)
                counter += 1
                print(f'Подписались на {counter} чел.')
        d.swipe_ext("up", scale=0.7, duration=0.1)
        if not follow.exists():
            kill_proc += 1
            if kill_proc == 10:
                print('Элементы не найдены. Завершение работы программы')
                kill_app()
                exit()


def follow_by_some_profile():
    counter = 0
    kill_proc = 0
    follow = d(text='Подписаться', className='android.widget.TextView')
    while True:
        sleep(1)
        if follow.exists() in range(0, 7):
            for _ in follow:
                kill_proc -= kill_proc
                follow.click()
                sleep(1)
                counter += 1
                print(f'Подписались на {counter} чел.')
        d.swipe_ext("up", scale=0.7, duration=0.2)
        if not follow.exists():
            kill_proc += 1
            if kill_proc == 10:
                print('Элементы не найдены. Завершение работы программы')
                kill_app()
                exit()


def start_code():
    while True:
        print('1. Отписаться от невзаимных', '2. Добавить друзей', '3. Подписаться в ответ', '4. Подписаться вручную')
        start_input = input('Выбери номер работы: ')
        if start_input == '1':
            unfollow_non_followers()
        if start_input == '2':
            follow_new_guy()
        if start_input == '3':
            follow_followers()
        if start_input == '4':
            follow_by_some_profile()
        else:
            print('Что-то не то ввели...')


start_code()
