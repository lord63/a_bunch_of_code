# **Comics**

### 功能：

检查漫画是否更新，并通过飞信发送短信提醒。

### 依赖：

*  Requests

*  BeautifulSoup

### 使用：

在当前目录下新建文件`config.py`, 像这样：

    MOBILENUM = 'xxxx'    # 你的手机号码

    PASSWORD = 'xxx'      # 你的飞信的密码

然后`$python check_comics.py`就可以了。


### 参考：

飞信发送短信的函数来自[laomo](https://gist.github.com/laomo/c328834f23b26088b280#file-fetion-py)

