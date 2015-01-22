# Get_GPA

## 功能：

得到本学期的成绩和绩点

## 依赖：

* requests
* lxml
* prettytable

## 如何使用：

在当前目录下新建文件`config.py`, 像这样：

    STUDENTID = 'xxxx'   学号
    PASSWORD = 'xxxx'    密码

然后`$python get_grade.py` 就可以了

显示的效果大概是这样子的:

    $ python get_grade.py
    Logining...
    Login successfully.
    Get your marks successfully.
    +----------------+------+------+
    | 课程名称       | 学分 | 成绩 |
    +----------------+------+------+
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    | xxxxxxxxx      | x.x  |  xx  |
    +----------------+------+------+
    Your GPA is: x.xx
