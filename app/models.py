# db是在工厂函数__init__.py中实例化的SQLAlchemy()对象
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Flask-Login要求程序实现一个回调函数，使用特定的标识符加载用户
# Flask-Login会检查是否登录没有登录时会跳转到登录页
# 由于HTTP协议是无状态的，无法记录用户的访问状态
# 每次发起新请求时flask 会创建一个请求上下文，
# 在分发路由时flask-login根据cookie判断用户并绑定到当前的请求上下文。
# 由于这种绑定关系的存在，那么每次新的请求发生时都需要获取user
# 那么load_user其作用就是每次新请求时调用该方法获取user并绑定到当前的请求上下文，
# 绑定的意义在于每次当我们使用current_user的时候，会直接从当前上下文中返回。
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
