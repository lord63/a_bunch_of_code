#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.util import is_hop_by_hop
import socket

from flask import Flask, request
import flask
import requests


ALLOW_KEYS = ('xzSlE', 'ILbou', 'DukPL')
app = Flask(__name__)


@app.route('/')
def main():
    response = flask.Response()
    url, key, timeout = (request.args.get('u', ''), request.args.get('k', ''),
                         int(request.args.get('t', '30')))
    if key and key not in ALLOW_KEYS:
        return 'Invalid key!'

    if url and key:
        try:
            header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
                      rv:30.0) Gecko/20100101 Firefox/30.0",
                      "Accept": "text/html,application/xhtml+xml,\
                      application/xml;q=0.9,*/*;q=0.8"}
            r = requests.get(url, timeout=timeout, headers=header)
            header = {header: value for header, value in r.headers.items()
                      if not is_hop_by_hop(header)}
            cookie_added = False
            for header_name, header_value in header.items():
                if header_name == 'Set-Cookie' and cookie_added:
                    response.headers['Set-Cookie'] = header_value
                else:
                    response.headers['Set-Cookie'] = header_value
                    if header_name == 'Set-Cookie':
                        cookie_added = True
            return r.text
        except socket.timeout:
            pass
        except Exception as e:
            return repr(e)
    else:
        return "I need KEY and URL, check your fomat :("


if __name__ == '__main__':
    app.run()
