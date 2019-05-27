from contextlib import contextmanager
import json

from flask import url_for
import pytest


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
