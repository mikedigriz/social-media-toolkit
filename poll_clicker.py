from random import randint
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Автоматизация голосования на сайтах Блокнот. Так как нет авторизации - байпас легко получить сбросом печенек.

def poll_click():
    click = 0
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('/home/mikedigriz/chromedriver', options=options)
    # передаем url голосования
    driver.get('https://')
    sleep(2)
    while click < 310:
        try:
            sleep(randint(25, 130))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.find_element_by_id('vote_radio_answer1').click()
            click += 1
            print(f'Pressed:{click}')
            sleep(2)
            driver.delete_all_cookies()
            sleep(2)
            driver.refresh()
            sleep(2)
        except Exception as e:
            print(e)
            driver.delete_all_cookies()
            sleep(2)
            driver.refresh()
            continue
    driver.close()
    exit()


poll_click()
