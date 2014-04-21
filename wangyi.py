#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

import requests
from lxml import html


def download_photos(url):
    if url.endswith("pp.163.com/"):
        download_photo_collections(url)
    else:
        download_photo_collection(url)


def download_photo_collection(url):
    photo_urls, collection_title, author = get_collection_info(url)

    save_path = '/home/lord63/pictures/WangYi/' + author + "/" + collection_title
    if os.path.exists(save_path):
        pass
    else:
        os.makedirs(save_path)

    for photo_url, number in zip(photo_urls, range(len(photo_urls))):
        image_format = '.' + photo_url.split('.')[-1]
        picture_save_path = save_path + "/" + str(number) + image_format
        if os.path.isfile(picture_save_path):
            return
        r = requests.get(photo_url, stream=True)
        with open(picture_save_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    print "Successfully downloaded the collection: " + collection_title


def download_photo_collections(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    collection_urls = tree.xpath('//ul[@isshow="false"]/li/a[1]/@href')
    print "Successfully got the collection_urls\n"

    for colletion_url in collection_urls:
        download_photo_collection(colletion_url)
    print "\nPhoto collections have be downloaded :)"


def get_collection_info(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)

    photo_urls = tree.xpath('//div[@class="pic-area"]/img/@data-lazyload-src')

    raw_name = tree.xpath('//li[@class="o-box o-box-userinfo"]/h2/text()')
    name = ''.join(raw_name).strip()
    count = tree.xpath('//li[@class="o-box o-box-userinfo"]/p[1]/b/text()')
    collection_title = name + ''.join(count)

    raw_author = tree.xpath('//p[@class="picset-author"]/a[1]/text()')
    author = ''.join(raw_author)

    return photo_urls, collection_title, author


# ----------------------------------------------------------------------#

url = raw_input("Please input the url: ")
download_photos(url)
