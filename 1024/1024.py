#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import string
from codecs import open


def check(code):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux \
                            x86_64; rv:28.0) Gecko/20100101 Firefox/28.0',
                            'Referer': 'http://t66y.com/register.php'})
    data = {'action': 'reginvcodeck', 'reginvcode': code}
    r = session.post('http://t66y.com/register.php?', data=data)
    status = re.search(r"(?<=invcode\(')\d(?='\))", r.text).group()
    if status == '1':
        print '{0}: NO'.format(code)
    else:
        print '{0}: OK'.format(code)


def minus_one(codes):
    """数字都减一"""
    for i in range(len(codes)):
        code = list(codes[i])
        for j in range(len(code)):
            if code[j] in string.digits:
                code[j] = string.digits[string.digits.index(code[j]) - 1]
        codes[i] = ''.join(code)
    for code in codes:
        check(code)

def guess(codes):
    pass

if __name__ == '__main__':
    with open('code.txt', encoding='utf-8') as f:
        codes = f.read().split()
