"""
    Flask项目管理文件目录views
    管理数据路由，为前端请求的提交与获取数据提供一个数据定位
"""

from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


"""
    在蓝本中编写视图函数主要有两点不同：
        第一，和前面的错误处理程序一样，路由修饰器由蓝本提供；
        第二，url_for() 函数的用法不同。
            你可能还记得，url_for() 函数的第一个参数是路由的端点名，
            在程序的路由中，默认为视图函数的名字。
            例如，在单脚本程序中，index()视图函数的URL可使用url_for('index') 获取。
"""
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
