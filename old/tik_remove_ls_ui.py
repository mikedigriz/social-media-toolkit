from time import sleep

import uiautomator2 as u2

# Альтернативная реализация удаления личных сообщений TikTok. Используются id элементов.
# TikTok под каждую новую версию меняет id элементов.

# USB - Connection
d = u2.connect('R58M31BXMNT')  # get from "adb devices"


# WiFi - Connection
# d = u2.connect('192.168.1.130:5555')


def start_app():
    d.app_start('com.zhiliaoapp.musically', use_monkey=True, stop=True)


def kill_app():
    d.app_stop('com.zhiliaoapp.musically')


def remove_ls():
    counter = 0
    start_app()
    sleep(2)
    d(text="Я").click()
    sleep(0.5)
    d(text="Входящие").click()
    # direct button
    d(resourceId="com.zhiliaoapp.musically:id/aoa").click()
    sleep(2)
    while True:
        if d.xpath('//*[@resource-id="com.zhiliaoapp.musically:id/d7y"]/android.widget.LinearLayout[5]'):
            d.xpath('//*[@resource-id="com.zhiliaoapp.musically:id/d7y"]/android.widget.LinearLayout[5]').long_click()
            sleep(1)
            d(text='Удалить').click()
            sleep(0.5)
            d(text='Удалить').click()
            sleep(1)
            counter += 1
            print(f'Удалено чатов: {counter}')
        else:
            print(f'Чаты закончились!')
            exit()


remove_ls()
