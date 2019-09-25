import importlib
import logging
import os

from flask import Flask, Blueprint
from furl import furl
from raven.contrib.flask import Sentry
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
{% if cookiecutter.use_mail == 'y' -%}
from flask_mail import Mail
{% endif -%}


logger = logging.getLogger('factory')
logger.setLevel(logging.INFO)


db = SQLAlchemy()


def init_db(app):
    sqllogger = logging.getLogger('sqlalchemy.engine')
    sqllogger.setLevel(logging.CRITICAL)
    db.init_app(app)
    return db


{% if cookiecutter.use_mail == 'y' -%}
def init_mail(app):
    mail = Mail()
    mail.init_app(app)
    app.mail = mail
{% endif -%}


def init_config(app, config):
    """
    Init app config
    :param app:
    :param config: mapping or config file name
    :return:
    """
    if config and isinstance(config, dict):
        app.config.from_mapping(config)
    else:
        app.config.from_pyfile(config)


def init_sentry(app):
    if not app.debug:
        dsn = app.config.get('SENTRY_DSN')
        Sentry(app, dsn=dsn)


def init_migrations(app):
    return Migrate(app, db)


def register_blueprints(app, blueprint_names=None):
    try:
        blueprint_names = blueprint_names or os.listdir('app')
    except FileNotFoundError:
        logger.error('No app folder found, blueprints were not imported')
        return
    for name in blueprint_names:
        exists = os.path.exists(os.path.join('app', name, 'views.py'))
        if exists and not name.startswith('_'):
            views = importlib.import_module('app.%s.views' % name)
            blueprints = [v for v in views.__dict__.values() if isinstance(v, Blueprint)]
            for blueprint in blueprints:
                app.register_blueprint(blueprint)
        else:
            logger.info('Package %s has no views to import' % name)


def create_app(name=None, template_folder='templates', static_folder='static'):
    app = Flask(
        name or __name__.split('.')[0],
        template_folder=template_folder,
        static_folder=static_folder
    )
    return app


def init_app(app, config='config.py'):
    """
    :param app:
    :param config: mapping or config file name or None if config have been already inited
    :return:
    """
    if config:
        init_config(app, config=config)
    app.db = init_db(app)
    register_blueprints(app)
    init_sentry(app)
    init_migrations(app)
    return app


def create_db(dsn):
    engine, db_name = parse_dsn(dsn)
    logger.info('Creating DB:%s...' % db_name)
    conn = engine.connect()
    conn.execute('CREATE DATABASE %s;' % db_name)
    conn.close()


def create_tables(app):
    conn = app.db.session.connection()
    table_names = app.db.engine.dialect.get_table_names(connection=conn)
    if not table_names:
        logger.info('Creating tables...')
        app.db.create_all()
    else:
        logger.info('Tables are already created %s ' % table_names)


def drop_db(dsn):
    if is_db_exists(dsn):
        engine, db_name = parse_dsn(dsn)
        logger.info('Dropping DB:%s...' % db_name)
        conn = engine.connect()
        conn.execute('DROP DATABASE %s;' % db_name)
        conn.close()


def parse_dsn(dsn):
    f = furl(dsn)
    msg = 'No database name provided in DSN:%s' % dsn
    assert f.path.segments, msg
    assert f.path.segments[0], msg
    db_name = f.path.segments[0]
    # db_user = f.username
    f.path.remove(db_name)  # Remove database name from DSN
    engine = create_engine(f.url, isolation_level='AUTOCOMMIT')
    return engine, db_name


def is_db_exists(dsn):
    engine, name = parse_dsn(dsn)
    query = 'SELECT datname FROM pg_database WHERE datistemplate = false;'
    conn = engine.connect()
    names = {row[0] for row in conn.execute(query).fetchall()}
    conn.close()
    return name in names
