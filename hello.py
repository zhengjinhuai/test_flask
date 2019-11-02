import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell, Manager

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask类的构造函数只有一个参数——程序主模块或包的名字
app = Flask(__name__)
# 实现CSRF保护，设置一个密钥生成加密令牌，令牌验证请求中表单数据的真伪
# app.config存储框架、扩展和程序本身的配置变量
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://pythonista:1234@localhost/flasksql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # 追踪对象的修改
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 在请求结束时自动提交数据库数据,不用手动提交

# Flask扩展一般再创建程序实例时初始化
# Flask-Bootstrap, Flask-Moment 的初始化，
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # backref在关系的另一个模型中添加反向引用，使用role_id访问Role
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


def make_shell_context():
    """
        因为每次启动shell会话都需要导入数据库实例和模型
        因此让Flask-Script的Shell命令自动导入特定对象
        也就是不用总是自己from hello import User, Role
    """
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_shell_context()))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


if __name__ == '__main__':
    manager.run(debug=True)
