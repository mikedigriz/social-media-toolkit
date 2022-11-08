import csv
import random
import time
from time import sleep

import uiautomator2
import uiautomator2 as u2

# Да, это автоматизатор Тиндера или Знакомств VK. Тратить время на просмотр анкет? Не сегодня.
# Попутно можно собирать графу 'О себе'. Зачем? Просто.
# Язык приложения имеет значение.

file_time = time.strftime('_%m-%d %H-%M-%S')
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

blacklist_words = ['ребенок', 'Счастливая мама', 'бенд', 'Есть ребенок', 'сын', 'дочь', 'дочкой', 'жената',
                   'разведенка', 'Люблю тусовки',
                   'развелась', 'дочки', 'дочка', 'сынок', 'сынишка', 'дочурка',
                   'должен', 'тортики', 'абьюз', 'абьюзивные', 'люблю клубы', 'бизнес',
                   'модель', 'мать', 'Мама', 'мама', 'Trans', 'транс', 'хуй', 'ХУЙ', 'сотрудничество',
                   'скорпионша', '2 детей', '3 детей', 'двое детей', 'трое детей',
                   'просто так лайкать', 'просто общение', 'жених', 'такая как есть', 'скинуться', 'карликам',
                   'амбициозного', 'амбиции', 'вредная', 'капризная', 'ебанько', 'Веганка', 'веган', 'без отношений',
                   'Ищу друзей', 'ищу друзей', 'Я парень', 'кросик', 'заезжали', 'гетеро', 'Не ищу серьезных отношений',
                   'не ищу отношения']
bio_text = []


def start_app():
    d.app_start('com.vkontakte.android', stop=True, use_monkey=True)


def kill_app():
    d.app_stop('com.vkontakte.android')


def random_swipe_time():
    return random.uniform(0.03, 0.1)


def random_swipe_time_fast():
    return random.uniform(0.03, 0.09)


def double_click():
    random_value = random.randint(0, 1)
    if random_value == 1:
        return d.double_click(random.uniform(0.71, 0.87), random.uniform(0.341, 0.52))


def bypass_match():
    if d.xpath(
            '//*[@resource-id="match"]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.Button[1]').exists:
        d.xpath(
            '//*[@resource-id="match"]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.Button[1]').click()


def profile_is_end():
    if d(text="Анкеты закончились", className='android.widget.TextView')[1].exists:
        print('Анкеты закончились! Завершаем работу')
        return True


def screenshot():
    """Делает скриншот"""
    d.screenshot("./img/screenshot.jpg")


def start_code():
    # TODO start app
    # TODO counter for swipe
    swipe_good_counter = 0
    swipe_bad_counter = 0
    with open('Био_вк' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Биографии:'])
        while True:
            try:
                sleep(0.5)
                # check on active
                if profile_is_end():
                    break
                bypass_match()

                if d(className='android.widget.TextView')[3].exists(timeout=0.2):
                    bio_checker = d(className='android.widget.TextView', index=3).info
                    get_len_bio = len(bio_checker['text'])
                    print(f"ТЕКСТ био | {bio_checker['text']}")
                    # TODO replace symbol; may be add sleep?
                    bio_text.append(bio_checker['text'])
                    writer.writerow([bio_checker['text']])
                    double_click()
                    for blacklist in blacklist_words:
                        if blacklist in bio_checker['text']:
                            print(f"Стоп слово в био: {blacklist}")
                            d.swipe_ext("left", scale=0.7, duration=random_swipe_time_fast())
                            swipe_bad_counter += 1

                    if get_len_bio < 10:
                        print(f"Длина био короткая, {get_len_bio} символов!")
                        d.swipe_ext("left", scale=0.7, duration=random_swipe_time_fast())
                        double_click()
                        swipe_bad_counter += 1
                    else:
                        print(f"Сюда! [+{swipe_good_counter}/-{swipe_bad_counter}]")
                        double_click()
                        swipe_good_counter += 1
                        d.swipe_ext("right", scale=0.7, duration=random_swipe_time_fast())
                else:
                    d.swipe_ext("left", scale=0.7, duration=random_swipe_time_fast())
                    swipe_bad_counter += 1
            except uiautomator2.UiObjectNotFoundError:
                d.swipe_ext("left", scale=0.7, duration=random_swipe_time_fast())
                swipe_bad_counter += 1
                pass
            except KeyboardInterrupt:
                print(bio_text)
                sleep(1)
                exit()


def start_code_fast():
    """Более быстрая версия, чтобы не править код выше. Переиспользование да-да."""
    swipe_good_counter = 0
    swipe_bad_counter = 0
    with open('Био_вк' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Биографии:'])
        while True:
            try:
                # check on active
                if profile_is_end():
                    break

                # bypass match
                bypass_match()

                # check bio
                if d(className='android.widget.TextView')[3].exists(timeout=0.1):
                    bio_checker = d(className='android.widget.TextView', index=3).info
                    print(f"ТЕКСТ био | {bio_checker['text']}")
                    bio_text.append(bio_checker['text'])
                    writer.writerow([bio_checker['text']])
                    double_click()
                    for blacklist in blacklist_words:
                        if blacklist in bio_checker['text']:
                            print(f"Стоп слово в био: {blacklist}")
                            d.swipe_ext("left", scale=0.7, duration=random_swipe_time_fast())
                            swipe_bad_counter += 1
                    else:
                        print(f"Сюда! [+{swipe_good_counter}/-{swipe_bad_counter}]")
                        double_click()
                        swipe_good_counter += 1
                        d.swipe_ext("right", scale=0.7, duration=random_swipe_time_fast())
                # else:
                #     d.swipe_ext("left", scale=0.7, duration=random_swipe_time_fast())
                #     swipe_bad_counter += 1
            except uiautomator2.UiObjectNotFoundError:
                d.swipe_ext("right", scale=0.7, duration=random_swipe_time_fast())
                swipe_good_counter += 1
                print(f"Сюда! [+{swipe_good_counter}/-{swipe_bad_counter}]")
                pass
            except KeyboardInterrupt:
                print(bio_text)
                print(f"Сюда! [+{swipe_good_counter}/-{swipe_bad_counter}]")
                sleep(1)
                exit()


start_code_fast()
