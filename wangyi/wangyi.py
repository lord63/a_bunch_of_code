#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import requests
from bs4 import BeautifulSoup


def download_photos(given_url):
    if given_url.endswith("pp.163.com/") or given_url.endswith("pp.163.com"):
        download_photo_albums(given_url)
    else:
        download_photo_album(given_url)


def download_photo_album(album_url):
    photo_urls, album_title, author = get_album_info(album_url)

    main_dir_name = '/home/lord63/pictures/WangYi/'
    save_path = main_dir_name + author + "/" + album_title
    if os.path.exists(save_path):
        pass
    else:
        os.makedirs(save_path)

    for photo_url, number in zip(photo_urls, range(len(photo_urls))):
        image_format = '.' + photo_url.split('.')[-1]
        picture_save_path = save_path + "/" + str(number) + image_format
        if os.path.isfile(picture_save_path):
            return
        request = requests.get(photo_url, stream=True)
        with open(picture_save_path, "wb") as f:
            for chunk in request.iter_content(1024):
                f.write(chunk)
    print "Successfully downloaded the album: " + album_title


def download_photo_albums(homepage):
    page = requests.get(homepage)
    soup = BeautifulSoup(page.text)
    album_urls = []
    for album_url in soup.find_all('li', 'w-cover'):
        album_url = album_url.a['href']
        album_urls.append(album_url)
    print "Successfully got the album_urls\n"

    for album_url in album_urls:
        download_photo_album(album_url)
    print "\nPhoto albums have be downloaded :)"


def get_album_info(album_url):
    page = requests.get(album_url)
    soup = BeautifulSoup(page.text)

    photo_urls = []
    for photo_url in soup.find_all('div', 'pic-area'):
        photo_url = photo_url.img['data-lazyload-src']
        photo_urls.append(photo_url)

    name = soup.find(id='p_username_copy').string.strip()
    count = soup.find('p', 'picset-count').b.string
    album_title = name + ''.join(count)
    author = soup.find('p', 'picset-author').a.string

    return photo_urls, album_title, author

if __name__ == '__main__':
    URL = raw_input("Please input the url: ")
    download_photos(URL)
