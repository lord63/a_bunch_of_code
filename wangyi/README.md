# Wangyi

## 简介
一个下载[网易摄影][1]图册的小玩意，支持下载作者的全部专辑和单张专辑。

## 依赖
* Python2.7
* [Requests][2]
* [BeautifulSoup][4]

## 如何使用
1  修改`line20： the_main_dir`，这里放所有下载网易的图片，

2  运行它，`$ python wangyi.py`

3  按照提示输入，摄影者主页的链接是下载所有的专辑，某专辑的链接则是下载该专辑的

下载完成后的目录树应该像这样子：

    |
    |---the_main_dir
          |
          |---author's name
                |
                |---album's name
                        |
                        |---0.jpg
                        |---1.jpg
                        |...
                        |...


## License
MIT

[1]: http://pp.163.com/square  "网易摄影"
[2]: https://github.com/kennethreitz/requests  "Requests"
[4]: http://www.crummy.com/software/BeautifulSoup/  "BeautifulSoup"

