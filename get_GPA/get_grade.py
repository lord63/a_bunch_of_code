#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from os import path
import pickle
import getpass
import time
import subprocess
import sys

import requests
from lxml import html
from prettytable import PrettyTable


session = requests.Session()
# Change UA to a mobile UA, the task will be easier.
mobile_ua = {'User-Agent': "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 \
    like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) \
    Version/4.0 Mobile/7A341 Safari/528.16"}
session.headers.update(mobile_ua)


def process(tds):
    """得到成绩和学分

    返回的列表是这样的 [score, points, score, points, ...]
    """
    for td in tds:
        if isinstance(td, unicode):
            tds.remove(td)
    return [float(td) for td in tds]


def marks_to_points(td):
    """课程成绩到课程绩点之间的换算"""
    if 95 <= td <= 100:
        return 5.0
    elif 60 <= td <= 94:
        return (td-45)/10.0
    else:
        return 0


def save(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)


def load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def login(student_id, md5_password):
    """Login to the website: http://m.hdu.edu.cn/"""

    # To get the lt, a parameter which will be used to login.
    header_1 = {'Referer': 'http://www.hdu.edu.cn/m.html'}
    request_1 = requests.get(
        'http://cas.hdu.edu.cn/cas/login?service=http%3A%2F%2Fi.hdu.edu.cn%2F\
        dcp%2Findex.jsp', headers=header_1)
    tree_1 = html.fromstring(request_1.text)
    lt = tree_1.xpath('//div/input[@name="lt"]/@value')[0]

    # Login in
    # I add referer for all the get/post requests, in case the requests fails.
    header_2 = {'Referer': 'http://cas.hdu.edu.cn/cas/login?service=http%3A%2F\
                %2Fi.hdu.edu.cn%2Fdcp%2Findex.jsp'}
    login_url = 'http://cas.hdu.edu.cn/cas/login'
    login_data = {
        'encodedService': 'http%3a%2f%2fi.hdu.edu.cn%2fdcp%2findex.jsp',
        'service': 'http://i.hdu.edu.cn/dcp/index.jsp',
        'serviceName': 'null',
        'loginErrCnt': 0,
        'username': student_id,
        'password': md5_password,
        'lt': lt
    }
    request_2 = session.post(login_url, data=login_data, headers=header_2)
    tree_2 = html.fromstring(request_2.text)
    # Get the redirection link
    try:
        redirect_link = tree_2.xpath('//noscript/p/a/@href')[0]
        print 'Logining...'
    except IndexError:
        sys.exit("Check your password and student id.")

    # This redirection is essentional
    header_3 = {'Referer': 'http://cas.hdu.edu.cn/cas/login'}
    session.get(redirect_link, headers=header_3)

    # The main page, login in now
    session.get('http://i.hdu.edu.cn/dcp/xphone/m.jsp', headers=header_3)
    print 'Login successfully.'
    save(session.cookies, 'cookies')
    return session


def fetch_and_count(student_id, md5_password):
    cookies_path = path.dirname(path.realpath(__file__)) + '/cookies'
    # Get your marks
    header_5 = {'Referer': 'http://i.hdu.edu.cn/dcp/xphone/m.jsp'}

    if (path.exists(cookies_path) and
       (time.time() - path.getmtime(cookies_path) < 1500)):
            print 'Reload the cookies.'
            global session
            request_5 = session.get('http://i.hdu.edu.cn/dcp/xphone/cjcx.jsp',
                                    headers=header_5,
                                    cookies=load(cookies_path))
    else:
        if path.exists(cookies_path):
            print 'Cookies has expired, remove it.'
            subprocess.call(['rm', cookies_path])
        session = login(student_id, md5_password)
        request_5 = session.get('http://i.hdu.edu.cn/dcp/xphone/cjcx.jsp',
                                headers=header_5)
    print 'Get your marks successfully.'

    # TODO should we remove the log out?
    # Log out
    # SESSION.get('http://i.hdu.edu.cn/dcp/dcp/comm/jsp/logout.jsp',
    #             headers=header_5)

    # Procss the data contains your marks
    tree = html.fromstring(request_5.text)
    table_data = tree.xpath('//td[@class="xl1"]/text()')
    body = process(table_data[3:])
    total_credits = 0.0
    total_grade_points = 0.0

    for i in range(0, len(body), 2):
        total_credits += body[i]
        total_grade_points += body[i] * marks_to_points(body[i+1])
    gpa = round(total_grade_points/total_credits, 4)

    # Print your scores in a table:
    table = PrettyTable(table_data[:3])
    table.align[table_data[0]] = "l"
    table.padding_width = 1
    for i, td in zip(range(3, len(table_data), 3), table_data):
        table.add_row(table_data[i:i+3])
    print table
    print 'Your GPA is: %.4f' % gpa


def main():
    login_info_path = path.dirname(path.realpath(__file__)) + '/login_info'
    cookies_path = path.dirname(path.realpath(__file__)) + '/cookies'
    if len(sys.argv) > 1 and sys.argv[1] == 'new':
        if path.exists(login_info_path):
            subprocess.call(['rm', login_info_path])
        if path.exists(cookies_path):
            subprocess.call(['rm', cookies_path])
    if not path.exists(login_info_path):
        student_id = raw_input('Student_ID: ')
        password = getpass.getpass()
        md5_password = hashlib.md5(password).hexdigest()
        save({'student_id': student_id, 'password': md5_password},
             login_info_path)
    else:
        md5_password, student_id = load('login_info').values()
    fetch_and_count(student_id, md5_password)


if __name__ == '__main__':
    main()
