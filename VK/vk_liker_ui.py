from time import sleep

import uiautomator2 as u2

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
heightUp = height / 2
vk_massive = ['@postnews', '@sysodmins', '@tproger']


def start_app():
    d.app_start('com.vkontakte.android', stop=True, use_monkey=True)


def kill_app():
    d.app_stop('com.vkontakte.android')


def go_like():
    """Последовательно ставит лайки в заданные сообщества"""
    for _ in vk_massive:
        start_app()
        d(resourceId="com.vkontakte.android:id/smallLabel", text="Сервисы").click()
        d(resourceId="com.vkontakte.android:id/title", text="Сообщества").click()
        d.xpath('//*[@resource-id="com.vkontakte.android:id/search_milkshake_background"]/android.view.View[1]').click()
        d.xpath(
            '//*[@resource-id="com.vkontakte.android:id/search_milkshake_background"]/android.view.View[1]').set_text(_)
        sleep(1)
        d.xpath('//*[@resource-id="com.vkontakte.android:id/recycler"]/android.view.ViewGroup[1]').click()
        sleep(1)
        counter = 0
        kill_proc = 0
        like = d(selected='false', resourceId='com.vkontakte.android:id/iv_likes',
                 className='android.widget.ImageView')
        while True:
            if like.exists() in range(0, 2):
                for _ in like:
                    kill_proc -= kill_proc
                    like.click()
                    sleep(1)
                    counter += 1
                    print(f'Поставлено лайков: {counter}')
            d.swipe_ext("up", scale=0.7, duration=0.1)
            sleep(1)
            if not like.exists():
                kill_proc += 1
                if kill_proc == 8:
                    print(f'Элементы не найдены. Завершение работы программы для {_}')
                    kill_app()
                    break


def go_like_my_girl():
    """Тот непонятный случай когда тебе нужно лайкать какого-то человека постоянно"""
    start_app()
    d(resourceId="com.vkontakte.android:id/smallLabel", text="Сервисы").click()
    d(resourceId="com.vkontakte.android:id/title", text="Друзья").click()
    d(resourceId="com.vkontakte.android:id/fl_bg_left_part").click()
    # поменяй @my_girl_id на нужный
    d(resourceId="com.vkontakte.android:id/fl_bg_left_part").set_text('@my_girl_id')
    sleep(1)
    d.xpath('//*[@resource-id="com.vkontakte.android:id/recycler"]/android.view.ViewGroup[1]').click()
    sleep(1)
    counter = 0
    kill_proc = 0
    like = d(selected='false', resourceId='com.vkontakte.android:id/iv_likes',
             className='android.widget.ImageView')
    while True:
        if like.exists() in range(0, 2):
            for _ in like:
                kill_proc -= kill_proc
                like.click()
                sleep(1)
                counter += 1
                print(f'Поставлено лайков: {counter}')
        d.swipe_ext("up", scale=0.7, duration=0.1)
        sleep(1)
        if not like.exists():
            kill_proc += 1
            if kill_proc == 8:
                print('Элементы не найдены. Завершение работы программы')
                kill_app()
                break


go_like()
