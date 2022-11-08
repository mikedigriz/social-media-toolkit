# TikTok version: 19.3.4
import random
import time
from time import sleep

import uiautomator2 as u2

# Автоматизация основных действий TikTok.
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
heightUp = height / 92
global softban_like
softban_like = 0


def start_app():
    d.app_start('com.zhiliaoapp.musically', stop=True, use_monkey=True)


def kill_app():
    d.app_stop('com.zhiliaoapp.musically')


def like_softban_detect():
    if d(resourceId='com.zhiliaoapp.musically:id/aff', selected='False'):
        global softban_like
        softban_like += 1
        print(f'Вероятно софт-бан! #{softban_like}')
    if d(resourceId='com.zhiliaoapp.musically:id/aff', selected='True'):
        softban_like -= softban_like
    # print('Обнуляем софт-бан')
    if softban_like >= 3:
        print('Уперлись в софт-бан! Спим 30 минут!')
        sleep(1800)
        print('Выходим из спячки')


def ads_and_live_stream_checker():
    if d(text='Сейчас в эфире', className='android.widget.TextView').exists or \
            d(textContains='Скачать', className='android.widget.TextView') or \
            d(text='Нажмите, чтобы посмотреть эфир', className='android.widget.TextView').exists or \
            d(className='android.widget.TextView', resourceId='com.zhiliaoapp.musically:id/do').exists or \
            d(textContains='Реклама', className='android.widget.TextView') or \
            d(textContains='Участвовать', className='android.widget.TextView') or \
            d(textContains='Подробнее', className='android.widget.TextView'):
        d.swipe_ext("up", scale=0.7, duration=0.01)
        print('Упс, здесь реклама или трансляция')
        sleep(0.5)


def ads_and_live_stream_checker_for_followers():
    ads_and_live_stream_checker()
    if d(text='Подписки', resourceId='android:id/text1', className='android.widget.TextView', selected='False'):
        print('Переходим в подписки!')
        d(text='Подписки', resourceId='android:id/text1', className='android.widget.TextView').click()
        sleep(0.5)


def random_choice():
    bool_variants = ['True', 'False']
    print(random.choice(bool_variants))


def like_rec():
    start_app()
    count = 0
    while True:
        ads_and_live_stream_checker()
        ads_and_live_stream_checker()
        time.sleep(random.uniform(0.2, 0.7))
        if d(resourceId='com.zhiliaoapp.musically:id/aff', selected='False'):
            d.double_click(widthCenter, heightCenter, 0.05)
            count += 1
            print(f'Количество лайков: {count}')
            time.sleep(random.uniform(0.1, 0.3))
        sleep(1)
        like_softban_detect()
        d.swipe_ext("up", scale=0.7, duration=0.02)


def like_followers():
    start_app()
    d.xpath(
        '//android.widget.HorizontalScrollView/android.widget.LinearLayout[1]/androidx.appcompat.app.ActionBar-b[1]/android.widget.LinearLayout[1]').click()
    count = 0
    while True:
        #  ads_and_live_stream_checker_for_followers()
        if d(resourceId='com.zhiliaoapp.musically:id/aff', selected='False'):
            d.double_click(widthCenter, heightCenter, 0.05)
            count += 1
            print(f'Количество лайков: {count}')
        time.sleep(random.uniform(0.3, 1))
        like_softban_detect()
        d.swipe_ext("up", scale=0.7, duration=0.02)


def follow():
    # follows = 0
    bool_variants = ['True', 'False']
    # follow icon
    if d(resourceId="com.zhiliaoapp.musically:id/ayq").exists:
        do_follow = random.choice(bool_variants)
        if do_follow == 'True':
            d(resourceId="com.zhiliaoapp.musically:id/ayq").click()
            # follows += 1
            # print(f'[+] Подписок: {follows}')


def like_rec_with_follow():
    start_app()
    count = 0
    while True:
        ads_and_live_stream_checker()
        ads_and_live_stream_checker()
        sleep(0.5)
        d.double_click(widthCenter, heightCenter, 0.05)
        count += 1
        print(f'Количество лайков: {count}')
        time.sleep(random.uniform(0.1, 0.3))
        follow()
        time.sleep(random.uniform(0.2, 0.8))
        like_softban_detect()
        d.swipe_ext("up", scale=0.7, duration=0.02)


def send_comment():
    comments_massive = ['Круть👍', 'Ваще жир))', 'Приколбасно😲', 'Лайкосик тебе👍👍👍', 'В рек👍', '+++',
                        '👍👍👍', '⊂(◉‿◉)つ👍🌺', '⊂(◉‿◉)つ', 'ʕ ᵔᴥᵔ ʔ', '(´｡• ω •｡)', '(＠＾◡＾)', '(◕‿◕)', '(⌒‿⌒)', '👀',
                        '(ღ˘⌣˘ღ)',
                        '༼ つ ◕‿◕ ༽つ', '٩(｡•́‿•̀｡)۶', '(๑˘︶˘๑) нашел в рек', '(´･ᴗ･ ) это кто у меня в рек?',
                        '❤️( ◡‿◡ )ты врек',
                        '(*˘︶˘*).｡.:*❤️',
                        '{\__/}\n\
                        ( • . •)\n\
                        / >❤️супер♥️рек👍👍',
                        '＜￣｀ヽ、　　　　　　　／ ￣ ＞\n\
                        　ゝ、　　＼　／⌒ヽ,ノ 　 /´\n\
                        　　　ゝ、 （ ( ͡◉ ͜> ͡◉) ／\n\
                        　　 　　>　 　 　,ノ\n\
                        　　　　　∠_,,,/´',
                        'молодец, супер🙂', 'неплохо ( ͝סּ ͜ʖ͡סּ)', 'ну в рек тогда 😌', '😉', 'Привет 😀',
                        'хай ͠° ͟ل͜ ͡°',
                        'ты впорядке, Саня? ͠° ͟ل͜ ͡°', 'опа, пушечка подъехала ︻┻┳══━一・・👍',
                        'Нашел тебя в рек, значит это судьба😉', 'взаимно✌️', 'мяв ฅ^•ﻌ•^ฅ',
                        'дружу ¬‿¬', 'дружу-дружу🙂', '༼ つ ◕‿◕ ༽つ👍🌸🤝🤝🤝', 'одобряю)😎', 'кашерно😀',
                        'Вот он, топовый видос🙂',
                        'вот это топ👏', 'бугага🙂', 'ееебой👍', '(｡•̀ᴗ-)✧', '˙ᵕ˙',
                        'ก็็ʕ•͡ᴥ•ʔ ก้้', '෴❤️෴', '◟(ᵔ ̮ ᵔ)͜💐', '︵‿୨❤️୧‿︵', '❤️⊂ʕ•ᴥ•⊂ʔ', '-`❤️´-',
                        # 'возьми\n🧠  (－‸ლ)',
                        '⇱_[◨_◧]\\', 'хорошечно ส็็༼ ຈل͜ຈ༽ส้้', 'ʚʘ͜͡))❨', '/ᐠ-༝-ᐟ\\', '(~˘▾˘)~',
                        ',___,\n[O.o] - O RLY?\n/)__)\n-"--"-', '👁👄👁', "__@'-'", '͡👁‿👁', '📷']

    if d(resourceId="com.zhiliaoapp.musically:id/a62").exists():
        d(resourceId="com.zhiliaoapp.musically:id/a62").click()
        time.sleep(random.uniform(1.2, 1.7))
        # поле ввода
        if d(resourceId="com.zhiliaoapp.musically:id/a5r").exists:
            time.sleep(random.uniform(0.4, 0.6))
            d(resourceId="com.zhiliaoapp.musically:id/a5r").click()
            time.sleep(random.uniform(0.4, 0.6))
            d(resourceId="com.zhiliaoapp.musically:id/a5r").set_text(f'{random.choice(comments_massive)}')
            time.sleep(random.uniform(0.2, 0.7))
            # send button
            d(resourceId="com.zhiliaoapp.musically:id/a6d").click()
            time.sleep(random.uniform(0.5, 0.7))
            # X icon
            d(resourceId="com.zhiliaoapp.musically:id/nj").click()
        else:
            d(resourceId="com.zhiliaoapp.musically:id/nj").click()
            sleep(0.5)
            d.swipe_ext("up", scale=0.7, duration=0.02)


def like_followers_with_comment():
    start_app()
    d.xpath(
        '//android.widget.HorizontalScrollView/android.widget.LinearLayout[1]/androidx.appcompat.app.ActionBar-b[1]').click()
    count = 0
    comments = 0
    bool_variants = ['True', 'False']
    while True:
        ads_and_live_stream_checker_for_followers()
        ads_and_live_stream_checker_for_followers()
        # like icon
        if d(resourceId='com.zhiliaoapp.musically:id/aff', selected='False'):
            d.double_click(widthCenter, heightCenter, 0.05)
            count += 1
            print(f'Количество лайков: {count}')
        time.sleep(random.uniform(0.5, 1))
        like_softban_detect()
        do_comment = random.choice(bool_variants)
        if do_comment == 'True':
            send_comment()
            comments += 1
            print(f'[+] Комментов: {comments}')
        d.swipe_ext("up", scale=0.7, duration=0.02)


def like_rec_with_follow_and_comment():
    start_app()
    count = 0
    comments = 0
    bool_variants = ['True', 'False']
    while True:
        ads_and_live_stream_checker()
        ads_and_live_stream_checker()
        sleep(0.5)
        d.double_click(widthCenter, heightCenter, 0.05)
        count += 1
        print(f'Количество лайков: {count}')
        time.sleep(random.uniform(0.5, 1))
        like_softban_detect()
        follow()
        do_comment = random.choice(bool_variants)
        if do_comment == 'True':
            send_comment()
            comments += 1
            print(f'[+] Комментов: {comments}')
        sleep(0.9)
        d.swipe_ext("up", scale=0.7, duration=0.02)


def start_code():
    while True:
        print('1. Пролайкать реки', '2. Пролайкать подписчиков', '3. Пролайкать реки + подписаться',
              '4. Пролайкать подписчиков с комментами', '5. Пролайкать реки + подписаться + комм')
        start_input = input('Выбери номер работы: ')
        if start_input == '1':
            like_rec()
        if start_input == '2':
            like_followers()
        if start_input == '3':
            like_rec_with_follow()
        if start_input == '4':
            like_followers_with_comment()
        if start_input == '5':
            like_rec_with_follow_and_comment()
        else:
            print('Что-то не то ввели...')


start_code()
