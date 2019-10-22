from contextlib import contextmanager
import json
import functools
import logging

from flask import url_for
import pytest

from lib.factory import db
from flask_sqlalchemy import Model


logger = logging.getLogger('{{cookiecutter.app_name}}')


@contextmanager
def not_raises(e=None, msg=None):
    if e is None:
        exception = ClientException
    try:
        yield None
    except exception as ex:
        pytest.fail(msg=msg or 'Raises %s' % ex)


class Client:
    json_header = 'application/json'

    def __init__(self, app):
        self.app = app

    @staticmethod
    def _get_url(endpoint, **values):
        return url_for(endpoint=endpoint, **values)

    @staticmethod
    def _get_data(resp, check_status=None):
        if check_status:
            assert resp.status_code == check_status
        data = resp.data
        if resp.content_type == 'application/json':
            data = json.loads(resp.data)
        return data

    def send(self, endpoint, method, data=None, check_status=200, content_type=None, headers=None, **values):
        kwargs = {}
        url = self._get_url(endpoint=endpoint, **values)
        func = getattr(self.app.client, method)
        if data:
            kwargs['data'] = data
        if content_type:
            kwargs['content_type'] = content_type
        if headers:
            kwargs['headers'] = headers
        resp = func(url, **kwargs)
        return self._get_data(resp, check_status=check_status)

    def get(self, **kwargs):
        return self.send(method='get', **kwargs)

    def delete(self, **kwargs):
        return self.send(method='delete', **kwargs)

    def post(self, content_type=None, data=None, **kwargs):
        content_type = content_type or self.json_header
        if content_type == self.json_header:
            data = json.dumps(data)
        return self.send(method='post', data=data, content_type=content_type, **kwargs)

    def put(self, content_type=None, data=None, **kwargs):
        content_type = content_type or self.json_header
        if content_type == self.json_header:
            data = json.dumps(data)
        return self.send(method='put', data=data, content_type=content_type, **kwargs)


class ClientException(Exception):
    pass


def db_func_fixture(**kwargs):
    """
    Decorates fixture function which should return a function
    which in turn should create and return single or a list of
    db.Model instances
    :param kwargs: any params for pytest.fixture function
    :return:
    """
    def fixture_decorator(func):
        func = pytest.fixture(**kwargs)(func)

        @functools.wraps(func)
        def wrapped_fixture(*a, **kw):
            instances = []

            def func_decorator(f):
                @functools.wraps(f)
                def decorated_func(*a, **kw):
                    resp = f(*a, **kw)
                    err_msg = f'Function {func.__name__}->{f.__name__} should return db.Model instance(s)'
                    for instance in [resp] if not isinstance(resp, list) else resp:
                        assert issubclass(instance.__class__, Model), err_msg
                        instances.append(instance)
                    return resp

                return decorated_func

            yield func_decorator(func(*a, **kw))

            types = set()
            for i in instances:
                db.session.delete(i)
                types.add(i.__class__)
                logger.info('Deleted instance id:%s type:%s', i.id, i.__class__)
            db.session.commit()

        return wrapped_fixture
    return fixture_decorator

