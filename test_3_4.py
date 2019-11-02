"""
    1. 使用flask-bootstrap模板
    2. 自定义错误页面
"""
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # 返回响应的同时返回错误代码500
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
