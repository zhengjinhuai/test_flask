"""
    Blueprint是Flask项目的一种组件式开发；
    使用蓝图可以极大地简化大型应用的开发难度，
    也为Flask扩展 提供了一种在应用中注册服务的集中式机制。
    模块化管理程序路由是它的特色，它使程序结构清晰、简单易懂。

    Blueprint也可以定义路由；
    在蓝本中定义的路由处于休眠状态
    直到蓝本注册到程序上后，路由才真正成为程序的一部分。
    使用位于全局作用域中的蓝本时，定义路由的方法几乎和单脚本程序一样。
"""

from flask import Blueprint  # Flask中使用蓝图将功能与主服务分开

# 第一个参数为蓝本名字，第二个为蓝本所在的包或模块
main = Blueprint('main', __name__)

# 导入这两个模块就能把路由和错误处理程序与蓝本关联起来
# 注意，在app/main/__init__.py 脚本的末尾导入，这是为了避免循环导入依赖，
# 因为在views.py 和errors.py 中还要导入蓝本main。
from . import views, errors

# 蓝图仅仅记录了未来应该发生的操作， 而不是当即实现
# 蓝本在工厂函数create_app() 中注册到程序上

from ..models import Permission


# 1.app_context_processor作为一个装饰器修饰一个函数
# 2.函数的返回结果必须是dict，
#   届时dict中的key将作为变量在所有模板中可见。
# 3. 因为模板类中可能也需要检查权限，所以Permission类中的所有常量必须要能够在模板中访问
@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
