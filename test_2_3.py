"""
    1. 使用flask-scipt扩展Flask程序，把命令行解析功能添加到py文件
"""

from flask import Flask
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    """将index注册为路由

    处理URL和函数之间关系的程序称为路由
    index()这样的函数称为视图函数（view function）
    返回的是响应
    浏览器访问对应的URL之后，触发服务执行index()函数
    比如函数对应的的URL为http://127.0.0.1:5000/
    """
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    """这函数对应的的URL为http://127.0.0.1:5000/user/<name>"""
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    manager.run()
