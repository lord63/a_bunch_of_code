#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import call
import multiprocessing

import requests
from bs4 import BeautifulSoup


class WangYi(object):
    def __init__(self):
        self.main_dir = '/tmp/WangYi/'
        self.pending_queue = multiprocessing.JoinableQueue()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux \
            x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})

    def download_photos(self, given_url):
        if (given_url.endswith("pp.163.com/") or
                given_url.endswith("pp.163.com")):
            print 'Start download photo albums...'
            self.session.headers.update({'Referer': given_url})
            self.download_photo_albums(given_url)
        else:
            print 'Start download photo album...'
            self.session.headers.update({'Referer': 'http://pp.163.com/pp/'})
            self.download_photo_album(given_url)

    def download_photo_album(self, album_url):
        photo_urls, album_title, author = self.get_album_info(album_url)
        save_path = self.main_dir + author + "/" + album_title
        if os.path.exists(save_path):
            pass
        else:
            os.makedirs(save_path)

        for photo_url, number in zip(photo_urls, range(len(photo_urls))):
            image_format = '.' + photo_url.split('.')[-1]
            picture_save_path = save_path + "/" + str(number) + image_format
            if os.path.exists(picture_save_path):
                return
            self.pending_queue.put([picture_save_path, photo_url])
        print "\t" + album_title

    def download_photo_albums(self, homepage):
        page = self.session.get(homepage)
        soup = BeautifulSoup(page.text)
        album_urls = []
        for album_url in soup.find_all('li', 'w-cover'):
            album_url = album_url.a['href']
            album_urls.append(album_url)
        print "\nSuccessfully got the album_urls"

        for album_url in album_urls:
            self.download_photo_album(album_url)
        # print "Photo albums have be downloaded\n"

    def get_album_info(self, album_url):
        page = self.session.get(album_url)
        soup = BeautifulSoup(page.text)

        photo_urls = []
        for photo_url in soup.find_all('div', 'pic-area'):
            photo_url = photo_url.img['data-lazyload-src']
            photo_urls.append(photo_url)

        name = soup.find(id='p_username_copy').string.strip()
        if '/' in name:
            name = name.replace('/', '%')
        count = soup.find('p', 'picset-count').b.string
        album_title = (name + ''.join(count)).encode('utf-8')
        author = soup.find('p', 'picset-author').a.string.encode('utf-8')
        return photo_urls, album_title, author

    def get_download_location(self, given_urls):
        print '\nAll the photo albums have been downloaded :)'
        photo_albums_urls = [url for url in given_urls if
                             url.endswith("pp.163.com/") or
                             url.endswith("pp.163.com")]
        photo_album_urls = [
            url for url in given_urls if url not in photo_albums_urls]

        if photo_albums_urls:
            for photo_albums_url in photo_albums_urls:
                soup = BeautifulSoup(self.session.get(photo_albums_url).text)
                author = soup.find('h2', 'host-nname').a['title'].encode(
                    'utf-8')
                print 'Have a check your albums in {}{}/'.format(self.main_dir,
                                                                 author)
        if photo_album_urls:
            for photo_album_url in photo_album_urls:
                (photo_urls, album_title,
                 author) = self.get_album_info(photo_album_url)
                print 'Your single album in {}{}/{}'.format(
                    self.main_dir, author, album_title)

    def consumer(self):
        while True:
            item = self.pending_queue.get()
            # request = session.get(photo_url, stream=True)
            # with open(picture_save_path, "wb") as f:
                # for chunk in request.iter_content(1024):
                    # f.write(chunk)
            # call(['wget', '-q', '-T', '2', '-O', picture_save_path, photo_url])
            # call(['aria2c', '-o', picture_save_path, photo_url])
            call(['wget', '-q', '-T', '2', '-O', item[0], item[1]])
            self.pending_queue.task_done()


if __name__ == '__main__':
    wangyi = WangYi()
    q = wangyi.pending_queue
    consumer_1 = multiprocessing.Process(target=wangyi.consumer)
    consumer_2 = multiprocessing.Process(target=wangyi.consumer)
    urls = sys.argv[1:]
    if not urls:
        urls = raw_input("Input the url, separate with one space: ").split()
    for url in urls:
        wangyi.download_photos(url)
    consumer_1.daemon = True
    consumer_2.daemon = True
    consumer_1.start()
    consumer_2.start()
    q.join()
    wangyi.get_download_location(urls)
