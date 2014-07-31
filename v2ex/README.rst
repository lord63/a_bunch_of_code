v2ex\_daily\_mission
====================

功能：
------

模拟登录v2ex完成任务领钱 OvO

依赖：
------

-  Requests

-  Lxml

-  Terminal

如何使用：
----------

在\ ``/usr/local/bin/``\ 目录下新建文件\ ``v2ex_config.json``, 像这样：

    { “username” = ‘xxxx’, “password” = ‘xxxx’, “log\_directory” =
    ‘/path/to/save/logfile/’, “count” = 5, }

完成任务得到钱：

::

    $ v2ex_daily_mission

查看最近的情况(默认天数在 v2ex\_config.josn 的 count 中设置)：

::

    $ v2ex_daily_mission read 

也可以通过参数来查看最近的情况

::

    $ v2ex_daily_mission read -c NUMBER

通过 ``v2ex_daily_mission -h`` 和 ``v2ex_daily_mission read -h``
获得使用帮助

参考：
------

-  `1`_

-  `2`_

-  `3`_

License
-------

MIT

.. _1: http://www.v2ex.com/t/69166
.. _2: http://www.v2ex.com/t/80927
.. _3: http://www.v2ex.com/t/68549
