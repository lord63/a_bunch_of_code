#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

import requests
from config import Email, Password, Dirpath


def downlaod_songs(songs):
    for title, info in songs.items():
        r = requests.get(info['url'], stream=True)
        song_name = title.strip() + '_' + \
                    info['artist'].strip().replace('/', '&') + '.mp3'
        filename = Dirpath + song_name
        if os.path.isfile(filename):  
            return                  # if the song have downloaded, pass.
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print "get: " + song_name

# API reference: 
# http://zonyitoo.github.io/blog/2013/01/22/doubanfmbo-fang-qi-kai-fa-shou-ji/
# You can know more details about what those parameters means.
login_url = "http://www.douban.com/j/app/login"
login_data = {
    "app_name": "radio_desktop_win",
    "version": 100,
    "email": Email,
    "password": Password
}

s = requests.session()
r = s.post(url=login_url, data=login_data)

param = {
    "app_name": "radio_desktop_win",
    "version": 100,
    "type": "n",
    "channel": -3,  # My_redheart_channel
    "user_id": r.json()["user_id"],
    "token": r.json()["token"],
    "expire": r.json()["expire"]
}

songs = {}
for n in range(5):
    q = s.get('http://www.douban.com/j/app/radio/people', params=param)
    for i in range(44):  # the song number in a json, not always the same.
        try:
            song_title = q.json()['song'][i]['title']
            if "song_title" in songs:
                pass
            else:
                song_url = q.json()['song'][i]['url']
                song_artist = q.json()['song'][i]['artist']
                # the dict should look like this:
                # {song_title: {url: song_url, artist: song_artist}, ......}
                songs[song_title] = {'url': song_url, 'artist': song_artist}            
        except IndexError:
            break
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            q = s.get('http://www.douban.com/j/app/radio/people', params=param)
    print "I've found %d songs." % len(songs)
    time.sleep(5)

print "Start to download......"
downlaod_songs(songs)
print "\nOk. Have a look at here --> " + Dirpath + "  :)"
