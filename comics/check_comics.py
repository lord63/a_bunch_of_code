#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from os import path
from datetime import date
import sys

import requests
from bs4 import BeautifulSoup
from config import MOBILENUM, PASSWORD

connect = sqlite3.connect(path.join(sys.path[0], 'comics.db'))
cursor = connect.cursor()

def check(current_num):
    try:
        cursor.execute('SELECT * FROM comics WHERE number=?', (current_num,))
    except sqlite3.OperationalError:
        cursor.execute('CREATE TABLE comics (number text, date text)')
        return False
    else:
        return False if cursor.fetchone() is None else True

# This function is written by laomo
# https://gist.github.com/laomo/c328834f23b26088b280#file-fetion-py
def send_message(msg):
    url_space_login = 'http://f.10086.cn/huc/user/space/login.do?m=submit&fr=space'
    url_login = 'http://f.10086.cn/im/login/cklogin.action'
    url_sendmsg = 'http://f.10086.cn/im/user/sendMsgToMyselfs.action'
    parameter= {'mobilenum': MOBILENUM, 'password': PASSWORD}
    session = requests.Session()
    session.post(url_space_login, data=parameter)
    session.get(url_login)
    session.post(url_sendmsg, data={'msg':msg})

today = date.today().isoformat()
naruto_comics = 'http://www.tvimm.com/NARUTO.html'
r = requests.get(naruto_comics)
soup = BeautifulSoup(r.text)
href = soup.find('a', target='_blank')['href']
num = href.split('/')[-1]

if check(num):
    c = cursor.execute('SELECT * FROM comics WHERE number=?', (num,))
    latest_volumn, lastest_update_date = c.fetchone()
    print 'NARUTO: not updated yet, still stays at', latest_volumn 
    print 'Recently it was updated on', lastest_update_date
else:
    print 'NARUTO: has been updated to', num
    print 'Click here--> ' + 'http://www.tvimm.com' + href
    send_message('Naruto has been updated to ' + num)
    cursor.execute('INSERT INTO comics VALUES (?, ?)', (num, today))
    connect.commit()


