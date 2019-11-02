from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Flask类的构造函数只有一个参数——程序主模块或包的名字
app = Flask(__name__)
# 实现CSRF保护，设置一个密钥生成加密令牌，令牌验证请求中表单数据的真伪
# app.config存储框架、扩展和程序本身的配置变量
app.config['SECRET_KEY'] = 'hard to guess string'

# Flask扩展一般再创建程序实例时初始化
# Flask-Bootstrap, Flask-Moment 的初始化，
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            # 如果两次提交的名字不一样则调用flash()函数
            # 仅调用flash()不能渲染消息
            # Flask把get_flashed_messages()函数开放给模板
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # 生成http重定向响应
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    app.run(debug=True)
