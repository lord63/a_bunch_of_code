## Wangyi 

### 简介
一个下载[网易摄影][1]图册的小玩意，支持下载作者的全部专辑和单张专辑。

### 依赖
* Python2.7
* [Requests][2]
* [Lxml][3]
* [BeautifulSoup][4]

### 如何使用
1  修改`line20： the_main_dir`，这里放所有下载网易的图片，
  以摄影作者为名的子文件夹在其下面，举个例子：![][5]
  ---
  ---
  图集文件夹的以名字+张数命名，放在作者为名的文件夹的下面。举个例子：![][6]
  ---
  ---
  图片以数字加后缀名命名。举个例子：![][7]
  ---
  ---
2  运行它，`$ python wangyi.py`

3  按照提示输入，摄影者主页的链接是下载所有的专辑，某专辑的链接则是下载该专辑的

### License
MIT

[1]: http://pp.163.com/square  "网易摄影"
[2]: https://github.com/kennethreitz/requests  "Requests"
[3]: https://github.com/lxml/lxml  "Lxml"
[4]: http://www.crummy.com/software/BeautifulSoup/  "BeautifulSoup"
[5]: ./src/001.png
[6]: ./src/002.png
[7]: ./src/003.png