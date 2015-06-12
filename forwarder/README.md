# Forwarder

## Intro

It's a simple http forwarder, powered by Flask. The idea was totally stolen from
[Forwarder][] which was written by cdhigh using [Bottle][], I use Flask to implement it.
It's mainly developed to forward ZhihuDaily's feed because Zhihu block the
requests form GAE. It should be worked with [KindleEar][].

## Requirements

* Flask
* Requests

## Usage

make the url to be forwarded look like this:

    http://HOSTUTL/?k=KEY&t=TIMEOUT&u=URL
    k: valid keys.
    t: timeout, optional, default is 30s.
    u: url to be forwarded

For more details please check the [ZhihuDaily.py][]

## Reference

* [ZhihuDaily API][]
* [forwarder][] (can run on openshift)
* [ZhihuDailyForwarder][] (nodejs version)
* [issue#118][] (the reason why I wrote this)

[Bottle]: http://bottlepy.org/docs/stable/index.html
[End-to-end and Hop-by-hop Headers]: http://tools.ietf.org/html/rfc2616.html#page-92
[flask api proxy]: http://www.tanquach.com/flask-api-proxy/
[Forwarder]: https://github.com/cdhigh/Forwarder
[forwarder]: https://github.com/seff/forwarder
[issue#118]: https://github.com/cdhigh/KindleEar/issues/118
[KindleEar]: https://github.com/cdhigh
[ZhihuDaily API]: http://news.at.zhihu.com/api/1.2/news/latest
[ZhihuDaily.py]: https://github.com/cdhigh/KindleEar/blob/master/books/ZhihuDaily.py
[ZhihuDailyForwarder]: https://github.com/ohdarling/ZhihuDailyForwarder
