import os
import random
import time

# ТикТок автоматизация удаления личных сообщений
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
    while count <= 2:
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
    while count <= 2:
        time.sleep(random.uniform(1, 2))
        count += 1
        execute("input swipe " + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2 + ' ' + timesec)


def longpress():
    execute("input touchscreen swipe 554 1110 554 1110 1200")


def tap():
    execute("input tap 565 2065")
    time.sleep(random.uniform(0.01, 0.02))
    execute("input tap 735 1350")


swipe_down()
swipe_up()
if __name__ == '__main__':
    while True:
        longpress()
        time.sleep(random.uniform(0.01, 0.02))
        tap()
