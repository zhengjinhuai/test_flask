from flask import Flask

"""
    1. 所有Flask程序都必须创建一个程序实例
    2. Flask类的构造函数只有一个必须指定的参数, 即程序主模块或包的名字
    3. Flask 用这个参数决定程序的根目录，
    4. 以便稍后能够找到相对于程序根目录的资源文件位置。
"""
app = Flask(__name__)  # 创建一个Flask类的对象


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


# @app.route('/')
# def index():
#     """视图返回400状态码"""
#     return '<h1>Bad Request!</h1>', 400


if __name__ == '__main__':
    # 启动服务器
    app.run(debug=True)  # 启动服务器之后会进入轮询，等待并处理请求
