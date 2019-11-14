from flask import Blueprint

api = Blueprint('api', __name__)

# 导入python文件，其实就是运行导入的那个文件
from . import authentication, posts, users, comments, errors

