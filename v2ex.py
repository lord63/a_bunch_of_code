#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from lxml import html
from v2ex_config import USER, PASSWD


def get_once(page_text):
    tree = html.fromstring(page_text)
    once = tree.xpath('//input[@name="once"]/@value')[0]
    return once


def login(url):
    r = s.get(url, verify=False)
    login_data = {
        'u': USER,
        'p': PASSWD,
        'once': get_once(r.text),
        'next': '/'
    }
    headers = {'Referer': 'https://www.v2ex.com/signin'}
    s.post(url, headers=headers, data=login_data)


def get_money(mission_url):
    r = s.get(mission_url, verify=False)
    tree = html.fromstring(r.text)

    raw_once = tree.xpath('//input[@type="button"]/@onclick')[0]
    once = raw_once.split('=', 1)[1].replace(';', '').replace("'", '').strip()
    url = 'https://www.v2ex.com' + once
    if once == '/balance':
        print "You have completed the mission today."
        return
    else:
        s.get(url, verify=False)
        get_balance(balance_url)


def get_balance(balance_url):
    r = s.get(balance_url, verify=False)
    tree = html.fromstring(r.text)
    total = tree.xpath('//table[@class="data"]/tr[2]/td[4]/text()')[0]
    today = tree.xpath('//table[@class="data"]/tr[2]/td[5]/span/text()')[0]
    print "Today: " + today
    print "Total: " + total


s = requests.session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
                   rv:28.0) Gecko/20100101 Firefox/28.0'})

signin_url = 'https://www.v2ex.com/signin'
balance_url = 'https://www.v2ex.com/balance'
mission_url = 'https://www.v2ex.com/mission/daily'

login(signin_url)
get_money(mission_url)







