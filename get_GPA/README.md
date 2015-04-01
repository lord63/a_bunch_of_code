# Get_GPA

## 功能：

得到本学期的成绩和绩点

## 依赖：

* requests
* lxml
* prettytable
* python2.7

## 如何使用：

安装依赖: `pip install -r requirements.txt`

`$python get_grade.py` 就可以了, 第一次运行需要你输入学号和密码。

显示的效果大概是这样子的:

    $ python get_grade.py
    Logining...
    Login successfully.
    Get your marks successfully.
    +----------------+------+------+
    | 课程名称        | 学分  | 成绩  |
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

使用 `$python get_grade.py new` 来获得另一个人的成绩绩点。
