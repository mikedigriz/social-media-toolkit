from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Генерация токенов для нескольких акков. Можно использовать вечный токен VK

# Пары пароль\логин
passwords = ['35G8']
logins = ['+7926']

for passs, log in zip(passwords, logins):
    get_token_url = 'https://oauth.vk.com/authorize?client_id=******&scope=wall,groups&response_type=token&v=5.131'
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('/home/mikedigriz/chromedriver', options=options)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.get(get_token_url)
    sleep(2)
    email = driver.find_element_by_name('email')
    email.click()
    email.clear()
    email.send_keys(log)
    sleep(2)
    password = driver.find_element_by_name('pass')
    password.click()
    password.clear()
    password.send_keys(passs)
    button = driver.find_element_by_id('install_allow').click()
    print(driver.current_url[45:130])
    sleep(1)
    driver.delete_all_cookies()
    sleep(2)
    driver.close()
    sleep(10)
