## Redheart_doubanfm

### What it is
A python script to download the song you marked from doubanfm with the [Requests][1] module.

### Requirements
* Python 2.7
* Requests

### How to use
1. Edit the `config.py`
2. Just run it: `$ python get_liked_songs.py`

### API Reference
* [reference 1][2]
* [reference 2][3]

### Attention
* It still have a **bug**: It can't download all you liked songs. For example,
  I can only download 71 songs of my 75 likes songs. That because I get the
  download link of a song from the "我的红心兆赫" while you can't get all the
  donwload links at one time. With sending several requests, you will get some
  duplicated songs. With enough times, you may get all the songs, or not, I can't
  promise you that. If you know how to fix it, please help.

### License
MIT


[1]: https://github.com/kennethreitz/requests "Requests"
[2]: http://zonyitoo.github.io/blog/2013/01/22/doubanfmbo-fang-qi-kai-fa-shou-ji/
[3]: https://github.com/akfish/fm-terminal/blob/develop/douban-fm-api.md
