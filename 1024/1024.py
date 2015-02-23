#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import string
from codecs import open


def get_codes():
    """从文本中得到邀请码，不属于字母数字的使用 '*' 代替"""
    with open('code.txt', encoding='utf-8') as f:
        codes = f.read().split()
    for i in range(len(codes)):
        for alpha in codes[i]:
            if alpha not in string.digits and alpha not in string.lowercase:
                codes[i] = codes[i].replace(unicode(alpha), '*')
    return codes


def check(code):
    """检测 code 是否还未被注册"""
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux \
                            x86_64; rv:28.0) Gecko/20100101 Firefox/28.0',
                            'Referer': 'http://t66y.com/register.php'})
    data = {'action': 'reginvcodeck', 'reginvcode': code}
    r = session.post('http://t66y.com/register.php?', data=data)
    # 通过判断响应中的 parent.retmsg_invcode('NUM') 中的数
    # 字来确认邀请码情况
    status = re.search(r"(?<=invcode\(')\d(?='\))", r.text).group()
    if status == '1':
        print '{0}: NO'.format(code)
    else:
        print '{0}: OK'.format(code)


def lets_rock(codes, cases=[2]):
    """一般情况，遮住邀请码一位或者几位
    codes: a list of codes
    cases:
        0: 只有数字
        1: 只有字母
        2: 数字和字母

    你可以为每个邀请码分别指定类型，也可以用一个数字说明是同一类型

    """
    the_list = [string.digits, string.lowercase,
                string.digits+string.ascii_lowercase]
    if len(cases) == 1:
        cases = cases * len(codes)
    for code, case in zip(codes, cases):
        asterisks = code.count('*')
        # 抹掉了 1 个位，一般情况都是这样
        if asterisks == 1:
            for i in the_list[case]:
                check(code.replace('*', i))
        # 抹掉了 2 个位，情况稍微有点多
        if asterisks == 2:
            for i in the_list[case]:
                for j in the_list[case]:
                    alpha_list = list(code)
                    alpha_list[alpha_list.index('*')] = i
                    alpha_list[alpha_list.index('*')] = j
                    check(''.join(alpha_list))
        # 抹掉了 3 个位，不予以考虑, 实际情况也很少
        if asterisks == 3:
            print "DAMN IT"


def minus_one(codes):
    """其他情况之一: 数字都减一后是正确邀请码"""
    for i in range(len(codes)):
        code = list(codes[i])
        for j in range(len(code)):
            if code[j] in string.digits:
                code[j] = string.digits[string.digits.index(code[j]) - 1]
        codes[i] = ''.join(code)
    for code in codes:
        check(code)


if __name__ == '__main__':
    codes = get_codes()
    # 请根据实际情况选择 cases 减少尝试的次数
    lets_rock(codes, [2])
