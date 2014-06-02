#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

import requests
from lxml import html
from config import STUDENTID, PASSWORD

s = requests.Session()
# Change to a mobile UA, I think this task will be easier via mobile.
s.headers.update({'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 \
    like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0\
     Mobile/7A341 Safari/528.16'})


# To get the lt, a parameter which will be used to login.
header1 = {'Referer': 'http://www.hdu.edu.cn/m.html'}
r1 = requests.get('http://cas.hdu.edu.cn/cas/login?service=http%3A%2F%2Fi.hdu.edu.cn%2Fdcp%2Findex.jsp', headers=header1)
tree1 = html.fromstring(r1.text)
lt = tree1.xpath('//div/input[@name="lt"]/@value')[0]


# Login in
md5_password = hashlib.md5(PASSWORD).hexdigest()
# I add referer for all the get/post requests, just in case the requests will fail.
header2 = {'Referer': 'http://cas.hdu.edu.cn/cas/login?service=http%3A%2F%2Fi.hdu.edu.cn%2Fdcp%2Findex.jsp'}
login_url = 'http://cas.hdu.edu.cn/cas/login'
login_data = {'encodedService': 'http%3a%2f%2fi.hdu.edu.cn%2fdcp%2findex.jsp',
              'service': 'http://i.hdu.edu.cn/dcp/index.jsp',
              'serviceName': 'null',
              'loginErrCnt': 0,
              'username': STUDENTID,
              'password0': PASSWORD,
              'password': md5_password,
              'lt': lt}
r2 = s.post(login_url, data=login_data, headers=header2)
tree2 = html.fromstring(r2.text)
link = tree2.xpath('//noscript/p/a/@href')[0]  # get the redirection link
print 'Logining...'


# This redirection is essentional
header3 = {'Referer': 'http://cas.hdu.edu.cn/cas/login'}
r3 = s.get(link, headers=header3)


# The main page, login in now
r4 = s.get('http://i.hdu.edu.cn/dcp/xphone/m.jsp', headers=header3)
print 'Login successfully.'


# The page which contains your marks 
header5 = {'Referer': 'http://i.hdu.edu.cn/dcp/xphone/m.jsp?'}
r5 = s.get('http://i.hdu.edu.cn/dcp/xphone/cjcx.jsp', headers=header5)
with open('/home/lord63/code/get_grade/3', 'w') as f:
    f.write(r5.text.encode('utf-8'))
print 'Get your marks successfully.'






