"""
    1. 重定向
"""
from flask import Flask
from flask import make_response
from flask import redirect
from flask import abort


app = Flask(__name__)


# @app.route('/')
# def index():
#     """ make_response() 可接受1个，2个或3个参数
#
#     :return: Response对象
#     """
#     response = make_response('<h1>This document carries a cookies!</h1>')
#     response.set_cookie('answer', '42')
#     return response


@app.route('/')
def index():
    """使用重定向的特殊响应类型"""
    return redirect('http://github.com/zhengjinhuai/')


@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello %s</h>' %user.name


if __name__ == '__main__':
    app.run()
