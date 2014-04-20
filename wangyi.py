#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

import requests
from lxml import html


def get_picset_urls(picalbum_url):
    page = requests.get(picalbum_url)
    tree = html.fromstring(page.text)

    picset_urls = tree.xpath('//li[@class="w-cover"]/a[@class=\
                             "name detail f-trans j-cover"]/@href')
    return picset_urls


def get_urls_and_title(picset_url):
    page = requests.get(picset_url)
    tree = html.fromstring(page.text)

    picture_urls = tree.xpath('//div[@class="pic-area"]/img/\
                              @data-lazyload-src')
    raw_picset_title = tree.xpath('//li[@class="o-box o-box-userinfo"]\
                                  /h2[@class="picset-title"]/text()')
    picset_title = ''.join(raw_picset_title).strip()
    return picture_urls, picset_title

def make_picture_directory(picset_title):
    picture_save_path = '/home/lord63/pictures/test/' + picset_title
    os.mkdir(picture_save_path)
    return picture_save_path
    print "Successfully made the directory"


def download_picsets(picset_urls):
    for picset_url in picset_urls:
        picture_urls, picset_title = get_urls_and_title(picset_url)

        picture_save_path = make_picture_directory(picset_title)

        download_pictures(picture_urls, picture_save_path)


def download_pictures(picture_urls, picture_save_path):
    for picture_url, i in zip(picture_urls, range(len(picture_urls))):
        r = requests.get(picture_url, stream=True)
        with open(picture_save_path+"/"+str(i)+".jpg", "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


picalbum_url = "http://dingding147147.pp.163.com"
picset_urls = get_picset_urls(picalbum_url)
download_picsets(picset_urls)





