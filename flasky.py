import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role

# 如果已经定义了环境变量FLASK_CONFIG，则从中读取配置名；
# 否则使用默认配置。
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 然后初始化Flask-Migrate定义的上下文。
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
