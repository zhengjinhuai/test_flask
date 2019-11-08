from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

"""
    问题：此处为什么不直接使用current_app呢？:
    解答：Return the current object. This is useful if you want the real object behind the proxy at a time
        for performance reasons or because you want to pass the object into a different context.
        返回当前对象。如果出于性能原因或希望将对象传递到其他上下文中，一次需要代理后面的实例，则这非常有用。

    发邮件优化代码：https://www.cnblogs.com/santiego/p/10356001.html
"""


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
