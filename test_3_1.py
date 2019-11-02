"""
    1. 创建Jinja2模板并渲染它
"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    """Flask提供的render_template把Jinja2模块引擎集成到程序中

    render_template 函数的第一个参数是模板的文件名
    随后的参数都是键值对，表示模板中变量对应的真实值
    """
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


def main():
    app.run()


if __name__ == '__main__':
    main()
