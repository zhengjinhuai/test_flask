from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# 这段代码的解释：https://segmentfault.com/a/1190000020121091
def permission_required(permission):  # 每次调用permission_requireds时，都会定义一个新的内部函数decorated_function
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
