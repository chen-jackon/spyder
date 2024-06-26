import threading
import os
from src import redmine
import threading
import time


def rk(time):
    a = redmine.redmine('rk', time)
    a.checkout()


def aml(time):
    a = redmine.redmine('aml', time)
    a.checkout()


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')
    while 1:
        wait = int(input("设置等待时间(需大于3分钟)"))
        if wait > 2:
            wait = wait * 60
            break
        else:
            print("输入有误，请重新输入")

    while 1:
        try:
            res = input("请输入开启跟踪哪个redmine(aml/rk/all):")
            if res == "aml":
                aml(wait)
            elif res == 'rk':
                rk(wait)
            elif res == 'all':
                t1 = threading.Thread(target=rk)
                t2 = threading.Thread(target=aml)
                t1.start()
                t2.start()
                while 1:
                    time.sleep(1)
            else:
                print("输入有误请重新输入")

        except KeyboardInterrupt:
            break
