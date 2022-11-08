import time
from time import sleep

import uiautomator2 as u2

# Ставит лайки в аккаунты из списка

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

inst_list = ['@instagram_account_1', '@instagram_account_2', '@instagram_account_3']


def start_app():
    d.app_start('com.instagram.android', stop=True, use_monkey=True)


def kill_app():
    d.app_stop('com.instagram.android')


def go_like():
    for _ in inst_list:
        start_app()
        d.xpath('//*[@content-desc="Поиск и интересное"]/android.widget.ImageView[1]').click()
        sleep(1)
        d(resourceId="com.instagram.android:id/action_bar_search_hints_text_layout").click()
        sleep(1)
        d(className="android.widget.EditText").set_text(_)
        d.xpath('//*[@resource-id="com.instagram.android:id/recycler_view"]/android.widget.FrameLayout[1]').click()
        d(descriptionContains="в строке 1, столбце 1").click()
        counter = 0
        kill_proc = 0
        like = d(selected='false', resourceId="com.instagram.android:id/row_feed_button_like",
                 className='android.widget.ImageView')
        while True:
            if d(text='Реклама', resourceId='com.instagram.android:id/secondary_label',
                 className='android.widget.TextView').exists or \
                    d(text='Реклама', resourceId='com.instagram.android:id/row_feed_cta_wrapper',
                      className='android.widget.FrameLayout').exists:
                d.swipe_ext("up", scale=0.4, duration=0.05)
            if like.exists() in range(0, 4):
                for i in like:
                    kill_proc -= kill_proc
                    like.click()
                    sleep(0.5)
                    counter += 1
                    print(f'Поставлено лайков: {counter}')
            d.swipe_ext("up", scale=0.6, duration=0.05)
            if not like.exists():
                kill_proc += 1
                if kill_proc == 15:
                    print(f'Элементы не найдены {_}')
                    kill_app()
                    break


start_time = time.time()
go_like()
print("--- %s минут ---" % ((time.time() - start_time) / 60))
