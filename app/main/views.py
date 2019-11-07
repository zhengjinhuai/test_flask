"""
    Flask项目管理文件目录views
    管理数据路由，为前端请求的提交与获取数据提供一个数据定位
"""

from flask import render_template
from . import main


"""
    在蓝本中编写视图函数主要有两点不同：
        第一，和前面的错误处理程序一样，路由修饰器由蓝本提供；
        第二，url_for() 函数的用法不同。
            你可能还记得，url_for() 函数的第一个参数是路由的端点名，
            在程序的路由中，默认为视图函数的名字。
            例如，在单脚本程序中，index()视图函数的URL可使用url_for('index') 获取。
"""


@main.route('/')
def index():
    return render_template('index.html')
