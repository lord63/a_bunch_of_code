#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import requests
from bs4 import BeautifulSoup


def download_photos(url):
    if url.endswith("pp.163.com/") or url.endswith("pp.163.com"):
        download_photo_collections(url)
    else:
        download_photo_collection(url)


def download_photo_collection(url):
    photo_urls, collection_title, author = get_collection_info(url)

    main_dir_name = '/home/lord63/pictures/WangYi/'
    save_path = main_dir_name + author + "/" + collection_title
    if os.path.exists(save_path):
        pass
    else:
        os.makedirs(save_path)

    for photo_url, number in zip(photo_urls, range(len(photo_urls))):
        image_format = '.' + photo_url.split('.')[-1]
        picture_save_path = save_path + "/" + str(number) + image_format
        if os.path.isfile(picture_save_path):
            return
        r = requests.get(photo_url, stream=True)  # To get the raw content.
        with open(picture_save_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    print "Successfully downloaded the collection: " + collection_title


def download_photo_collections(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    collection_urls = []
    for url in soup.find_all('li', 'w-cover'):
        url = url.a['href']
        collection_urls.append(url)
    print "Successfully got the collection_urls\n"

    for colletion_url in collection_urls:
        download_photo_collection(colletion_url)
    print "\nPhoto collections have be downloaded :)"


def get_collection_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    photo_urls = []
    for url in soup.find_all('div', 'pic-area'):
        url = url.img['data-lazyload-src']
        photo_urls.append(url)

    name = soup.find(id='p_username_copy').string.strip()
    count = soup.find('p', 'picset-count').b.string
    collection_title = name + ''.join(count)
    author = soup.find('p', 'picset-author').a.string

    return photo_urls, collection_title, author

# ----------------------------------------------------------------------#

url = raw_input("Please input the url: ")
download_photos(url)