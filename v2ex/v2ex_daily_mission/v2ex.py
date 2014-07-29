#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import maketrans
import logging
import os
import sys
import json

import requests
from lxml import html
from terminal import Command


def get_once(page_text):
    tree = html.fromstring(page_text)
    once = tree.xpath('//input[@name="once"]/@value')[0]
    return once


def login(signin_url):
    r = s.get(signin_url, verify=False)
    login_data = {
        'u': config['username'],
        'p': config['password'],
        'once': get_once(r.text),
        'next': '/'
    }
    headers = {'Referer': 'https://www.v2ex.com/signin'}
    s.post(signin_url, headers=headers, data=login_data)


def get_money(mission_url):
    r = s.get(mission_url, verify=False)
    tree = html.fromstring(r.text)

    raw_once = tree.xpath('//input[@type="button"]/@onclick')[0]
    table = maketrans('', '')
    once = raw_once.split('=', 1)[1].translate(table, " ';")
    if once == '/balance':
        print "You have completed the mission today."
        return
    else:
        s.get('https://www.v2ex.com'+once, verify=False)
        get_balance(balance_url)


def get_balance(balance_url):
    r = s.get(balance_url, verify=False)
    tree = html.fromstring(r.text)
    total = tree.xpath('//table[@class="data"]/tr[2]/td[4]/text()')[0].strip()
    today = tree.xpath('//table[@class="data"]/tr[2]/td[5]/span/text()')[0].strip()
    logging.info('%-26sTotal:%-8s' % (today, total))
    print "Today: " + today
    print "Total: " + total


# command parse and set
command = Command('v2ex_daily_mission', 'complete the mission and get money')
command.option('-u, --username [username]', 'set your username, default read from config file')
command.option('-p, --password [password]', 'set your password, dafault read from config file')
command.option('-l, --log_directory [direcroty]', 'set the log direcroty, default read from config file')

# get config
with open('v2ex_config.json') as f:
    config = json.load(f)
if command.username is not None:
    config['username'] = command.username
if command.password is not None:
    config['password'] = command.password
if command['log_directory'] is not None:
    config['log_directory'] = command.log_directory

# subcommand
@command.action
def read(count=config['count']):
    """
    read log file

    :param count: read the count of the recent days
    :option count: -c, --count [count]
    """
    file_path = os.path.join(config['log_directory'], 'v2ex.log')
    os.system('tail -n {0} {1}'.format(count, file_path))
command.parse()

# set log
logging.basicConfig(
    filename=os.path.join(config['log_directory'], 'v2ex.log'),
    level='INFO',
    format='%(asctime)s [%(levelname)s] %(message)s')
# Disable log message from the requests library
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

s = requests.session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
                   rv:28.0) Gecko/20100101 Firefox/28.0'})

signin_url = 'https://www.v2ex.com/signin'
balance_url = 'https://www.v2ex.com/balance'
mission_url = 'https://www.v2ex.com/mission/daily'

def main():
    login(signin_url)
    get_money(mission_url)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
