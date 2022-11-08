import os
import random
import time

# ТикТок автоматизация кликов и свайпов
# Простая наивная реализация под конкретное устройство. Все параметры задаются по координатам.

adbShell = "adb shell {cmdStr}"


def execute(cmd):
    str = adbShell.format(cmdStr=cmd)
    print(str)
    os.system(str)


def swipe_up():
    x2 = str(random.randint(474, 541))  # начальные x
    y2 = str(random.randint(1270, 1310))  # начальные y
    x1 = str(random.randint(424, 450))  # конечные x
    y1 = str(random.randint(750, 885))  # конечные y
    timesec = str(random.randint(80, 120))  # скорость в мс
    count = 0
    while count <= 1:
        time.sleep(random.uniform(1, 2))
        count += 1
        execute("input swipe " + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2 + ' ' + timesec)


def swipe_down():
    x1 = str(random.randint(474, 541))  # начальные x
    y1 = str(random.randint(1270, 1310))  # начальные y
    x2 = str(random.randint(424, 450))  # конечные x
    y2 = str(random.randint(750, 885))  # конечные y
    timesec = str(random.randint(80, 120))  # скорость в мс
    count = 0
    while count <= 1:
        time.sleep(random.uniform(1, 2))
        count += 1
        execute("input swipe " + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2 + ' ' + timesec)


def swiper():
    x1 = str(510)  # начальные x
    y1 = str(1247)  # начальные y
    x2 = str(448)  # конечные x
    y2 = str(581)  # конечные y
    time = str(1500)  # скорость в мс
    execute("input swipe " + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2 + ' ' + time)


def sleeper():
    timer = time.sleep(random.uniform(0.5, 2))


def like():
    execute("input tap 828 453")
    sleeper()
    execute("input tap 828 680")
    sleeper()
    execute("input tap 828 920")
    sleeper()


swipe_down()
swipe_up()

if __name__ == '__main__':
    while True:
        swiper()
        like()
