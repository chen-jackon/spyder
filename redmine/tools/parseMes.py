import sys
import time

def parseUser():
    passwdPath = "./data/passwd.txt"
    with open(passwdPath, "r", encoding='utf-8') as f:
        tmp = f.readlines()
    res = []
    tmpL = []
    for i, n in enumerate(tmp):
        t = n.strip("\n").strip()
        if t == "":
            print('请补全"{}"文件中的信息.'.format(passwdPath))
            exit(-1)
        t = t.split(":")[-1]
        if i == 2:
            t.split(',')
            tmpL.append(t)
            res.append(tmpL)
        else:
            res.append(t)
    return res

def progress_bar(finish_tasks_number, tasks_number):
    """
    进度条

    :param finish_tasks_number: int, 已完成的任务数
    :param tasks_number: int, 总的任务数
    :return:
    """

    percentage = round(finish_tasks_number / tasks_number * 100)
    print("\r等待刷新: {}%: ".format(percentage), "▓" * (percentage // 2), end="")
    sys.stdout.flush()

