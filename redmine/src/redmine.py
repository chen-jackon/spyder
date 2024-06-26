import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
import random
import requests
from bs4 import BeautifulSoup
import re
import json
import os
import urllib
#import sys
#sys.path.append('..')
from tools import parseMes


class redmine(object):
    def __init__(self, vendor, time):
        self.__vendor = vendor
        if vendor == "rk":
            self.__login_url = 'https://redmine.rock-chips.com/login'
            print("正在初始化信息....")
            self.__urlListsFile = './data/rkUrlList.txt'
            self.__dataFile = './data/rkdata.json'
            if not os.path.exists(self.__urlListsFile):
                with open(self.__urlListsFile, 'w') as f:
                    pass
            with open(self.__urlListsFile, 'r') as f:
                self.__urlList = f.readlines()

            if not os.path.exists(self.__dataFile):
                with open(self.__dataFile, 'w') as f:
                    f.write("{}")
            with open(self.__dataFile, "r") as f:
                self.__histroy = json.load(f)
            usrMes = parseMes.parseUser()
            self.__emailUsername, self.__emailPasswd, self.__emailRecivers = usrMes

            self.__redmineUsername = "skg_sy"  # redmine 帐号
            self.__redminePassword = "skg_syskg_sy"  # redmine 密码
            self.__userNameContain = "商用"
            self.__verify = True
        elif vendor == 'aml':
            self.__login_url = 'https://support.amlogic.com/login'
            self.__urlListsFile = "./data/amlurlList.txt"
            self.__dataFile = "./data/amldata.json"
            if not os.path.exists(self.__urlListsFile):
                with open(self.__urlListsFile, 'w') as f:
                    pass
            with open(self.__urlListsFile, 'r') as f:
                self.__urlList = f.readlines()

            if not os.path.exists(self.__dataFile):
                with open(self.__dataFile, 'w') as f:
                    f.write("{}")
            with open(self.__dataFile, "r") as f:
                self.__histroy = json.load(f)

            usrMes = parseMes.parseUser()
            self.__emailUsername, self.__emailPasswd, self.__emailRecivers = usrMes
            self.__redmineUsername = "shawh_xiao"  # redmine 帐号
            self.__redminePassword = "AVT.KTC.BDS"  # redmine 密码
            self.__userNameContain = 'xiao'
            self.__verify = False
        else:
            print('请选择正确的供应商(rk/aml)')
            self.__exitE()
        self.__sleepTime = time
        try:
            self.__emailLogin()
            print("邮箱验证成功")
        except Exception as e:
            print(e)
            print("邮箱验证失败，请检查邮箱账户")
            self.__exitE()
    def __sleep(self):
        for i in range(0, self.__sleepTime):
            parseMes.progress_bar( self.__vendor, i, self.__sleepTime)
            time.sleep(1)
        print("\n")
    # 登陆
    def __login(self):
        if self.__vendor == 'rk':
            headers = {
                'Accept-Encoding': 'gzip,deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'redmine.rock-chips.com',
                'Origin': 'https//redmine.rock-chips.com',
                'Referer': 'https://redmine.rock-chips.com/login',
                'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/112.0.0.0Safari/537.36'}
            # 定义登录页面的URL
            self.__login_url = 'https://redmine.rock-chips.com/login'
            # 创建一个Session对象
            self.session = requests.Session()
            # 发送登录请求
            html = self.session.get(self.__login_url, headers=headers).text
            # with open("../222.html", 'w') as f:
            #     f.write(html)
            # html = self.session.get(login_url, headers=headers).text
            htmlDoc = BeautifulSoup(html, 'html.parser')
            to = htmlDoc.find_all('meta')
            tok = to[-1]['content']
            datas = urllib.parse.urlencode({
                'utf8': '✓',
                'authenticity_token': tok,
                # 'back_url': '/issues/399004?tab=history',
                'username': self.__redmineUsername,
                'password': self.__redminePassword,
                'autologin': '1',
            }).encode('gbk')

            response = self.session.post(self.__login_url, data=datas, headers=headers, verify=self.__verify)
            # with open("../333.html", "w") as f:
            #     f.write(response.text)
            if response.status_code == 200:
                print('Login successful!')
                return 0
            else:
                print(response.status_code)
                print('Login failed!')
                self.__exitE()
        elif self.__vendor == 'aml':
            login_url = 'https://support.amlogic.com/login'
            headers = {
                'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/112.0.0.0Safari/537.36'}
            # 定义登录页面的URL

            # 创建一个Session对象
            self.session = requests.Session()
            datas = urllib.parse.urlencode({
                'utf8': '✓',
                # 'back_url': '/issues/399004?tab=history',
                'username': self.__redmineUsername,
                'password': self.__redminePassword,
            }).encode('gbk')

            response = self.session.post(login_url, data=datas, headers=headers, verify=False)
            # with open("../333.html", "w") as f:
            #     f.write(response.text)
            if response.status_code == 200:
                print('aml Login successful!')
                return 0
            else:
                print(response.status_code)
                print('aml Login failed!')
                self.__exitE()

    def __emailLogin(self):
        smtp_server = 'mail.ktc.cn'
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
        server.login(self.__emailUsername, self.__emailPasswd)
        server.quit()

    def __sendEmail(self, text: str):
        # 邮件内容
        message = MIMEText(text, 'plain', 'utf-8')
        message['From'] = Header('redmine', 'utf-8')
        message['To'] = Header(self.__emailUsername, 'utf-8')
        message['Subject'] = Header('redmine回复', 'utf-8')

        # 发送邮件
        smtp_server = 'mail.ktc.cn'
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=5)
        server.login(self.__emailUsername, self.__emailPasswd)
        server.sendmail(self.__emailUsername, self.__emailRecivers, message.as_string())
        server.quit()

    def __compare(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        # 找到包含id为"tab-content-history"的div
        if self.__vendor == "rk":
            tab_content_history_div = soup.find('div', {'id': 'history'})
        elif self.__vendor == "aml":
            tab_content_history_div = soup.find('div', {'id': 'history'})
        # 找到包含在"tab-content-history"中的所有div
        divs = tab_content_history_div.find_all('div', {'id': re.compile(r'^change-\d+$')})
        count = 0
        # 判断是否包含 用户名中的其中几个字
        for div in divs:
            h4_tag = div.find('h4')
            if h4_tag and self.__userNameContain not in h4_tag.text:
                count += 1
        return count, divs
        
    def __exitE(self):
        print("按回车退出...")
        input()
        exit(-1)

    def checkout(self):
        self.__login()

        while 1:
            if len(self.__urlList) == 0:
                print("请添加需要检测的单号网址到data对应的UrlList当中一行一个单号")
                break
            with open(self.__urlListsFile, 'r') as f:
                self.__urlList = f.readlines()
            for i, urll in enumerate(self.__urlList):
                try:
                    url = urll.strip("\n").strip("/")
                    res = self.session.get(url + "?tab=history", cookies=self.session.cookies)
                    if res.status_code == 200:
                        text = res.text
                        # with open('../111.html', 'w') as f:
                        #     f.write(text)
                        if ("注册" in text) or ("忘记密码" in text):
                            self.__login()
                            continue
                        count, divs = self.__compare(text)
                        print("正在检测{}, 当前回复个数为{}".format(url, count))
                        if url not in self.__histroy:
                            pass
                        # 更新当前的key-value dict
                        if url in self.__histroy and self.__histroy[url] != count:
                            print("{}有差异".format(url))  # 可以发送邮件提醒
                            sendText = url + '有更新，请及时查看' + '\n' + divs[-1].text
                            self.__sendEmail(sendText)
                        self.__histroy.update({url: count})

                        # 更新data
                        with open(self.__dataFile, 'w') as f:
                            json.dump(self.__histroy, f)
                except Exception as e:
                    print(e)
            self.__sleep()