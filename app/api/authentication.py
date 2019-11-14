from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


# 身份验证方法
# 由于每次请求都要传送用户凭据，API路由最好通过安全的HTTP对外开放，再传输中加密全部请求和响应
# verify_password方法使用了HTTPBasicAuth的verify_password回调，
# 她提供了最大程度的灵活性（暂时没法完全理解这个知识点）
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        # 密码为空，假定为匿名用户
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True # g是flask AppContext的一个全局变量，用于区分密码认证和令牌认证
        return g.current_user is not None
    # 如果两个都不为空，则用常规的验证方法
    user = User.query.filter_by(email=email_or_token.lower()).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False   # 为了让视图能区别两种身份验证方法，False为密码认证
    return user.verify_password(password)


# 默认情况下，flask-HTTPAuth会自动返回401状态码，即身份验证凭据不正确
# 为了与API返回的其他错误保持一致，自定义anth_error这个方法
@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# 对蓝本中的所有路由进行保护
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


# 生成身份验证令牌
@api.route('/tokens/', methods=['POST'])
def get_token():
    # g.current_user.is_anonymous是为了避免客户端使用旧令牌申请新令牌
    # g.token_used是表明如果已经申请令牌认证就拒绝请求
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
