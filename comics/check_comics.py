#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from os import path
import sys

import requests
from bs4 import BeautifulSoup

connect = sqlite3.connect(path.join(sys.path[0], 'comics.db'))
cursor = connect.cursor()

def check(current_num):
    try:
        cursor.execute('SELECT * FROM comics WHERE num="%s"' % current_num)
    except sqlite3.OperationalError:
        cursor.execute('CREATE TABLE comics (num text)')
        return False
    else:
        return False if cursor.fetchone() is None else True

naruto_comics = 'http://www.tvimm.com/NARUTO.html#1'
r = requests.get(naruto_comics)
soup = BeautifulSoup(r.text)
num = soup.find('a', target='_blank')['href'].split('/')[-1]
if check(num):
    print 'NARUTO: not updated yet.'
else:
    print 'NARUTO: has been updated to', num
    cursor.execute('INSERT INTO comics VALUES ("%s")' % num)
    connect.commit()


