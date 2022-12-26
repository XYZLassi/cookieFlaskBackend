__all__ = ['create_app', 'create_worker_app']

from flask import Flask
from .config import config


def create_worker_app(config_name: str = 'default') -> Flask:
    from .ext import db, migrate, socket

    app = Flask(__name__, static_folder='_static', static_url_path='/static', template_folder='_templates')
    conf = config[config_name] if config_name in config else config['default']
    app.config.from_object(conf)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    socket.init_app(app, message_queue=app.config.get('REDIS_URL'))

    register_redis(app)

    return app


def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__, static_folder='_static', static_url_path='/static', template_folder='_templates')
    conf = config[config_name] if config_name in config else config['default']
    app.config.from_object(conf)

    load_ext(app)
    load_errors(app)

    load_blueprints(app)

    load_cli(app)
    register_shellcontext(app)

    register_redis(app)

    register_docs(app)

    return app


def load_ext(app: Flask):
    from .ext import db, migrate, socket, login

    env = app.jinja_env
    env.add_extension('jinja2.ext.do')

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)

    if not app.config.get('TESTING', False):
        socket.init_app(app, manage_session=False, message_queue=app.config.get('REDIS_URL'), cors_allowed_origins="*")
    else:
        socket.init_app(app)


def load_errors(app: Flask):
    pass


def load_blueprints(app: Flask):
    from .filters import bp as bp_filters
    app.register_blueprint(bp_filters)


def load_cli(app: Flask):
    from .cli.user import bp_cli as bp_user
    app.register_blueprint(bp_user)


def register_redis(app: Flask):
    from redis import Redis
    import rq

    if app.config['TESTING']:
        from fakeredis import FakeStrictRedis
        app.redis = FakeStrictRedis()
        app.task_queue = rq.Queue('{{cookiecutter.redis_db}}', connection=app.redis, is_async=False)
        return

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('{{cookiecutter.redis_db}}', connection=app.redis)


def register_docs(app: Flask):
    pass


def register_shellcontext(app: Flask):
    from .ext import db

    def shell_context():
        """Shell context objects."""
        return {"db": db}

    app.shell_context_processor(shell_context)
