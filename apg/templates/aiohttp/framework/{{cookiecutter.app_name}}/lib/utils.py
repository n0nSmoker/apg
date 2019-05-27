import datetime
import importlib
import os

from aiohttp import web

from constants import INTERNAL_ERROR, VALIDATION_ERROR


class RouteTableDef(web.RouteTableDef):  # noqa
    def __init__(self, url_prefix=None):
        super().__init__()
        self.url_prefix = url_prefix

    def route(self, method, path, **kwargs):
        if self.url_prefix:
            path = self.url_prefix + path
        return super().route(method, path, **kwargs)


def add_routes(app):
    dirs = (d for d in os.listdir('app') if not d.startswith('_'))
    for dir_name in dirs:
        try:
            views = importlib.import_module(f'app.{dir_name}.views')
        except ModuleNotFoundError:
            continue
        routes = [v for v in views.__dict__.values() if isinstance(v, RouteTableDef)]
        for r in routes:
            app.add_routes(r)


def import_models():
    dirs = (d for d in os.listdir('app') if not d.startswith('_'))
    for dir_name in dirs:
        try:
            importlib.import_module(f'app.{dir_name}.models')
        except ModuleNotFoundError:
            continue


def jsonify(data, status=200, headers=None):
    headers = headers or {}
    headers['Server'] = 'ЖON-compatible'
    return web.json_response(
        data=data,
        status=status,

    )


def fail(*, code=INTERNAL_ERROR, title=None, detail=None, links=None, source=None, meta=None, status=500):
    if status == 400:
        code = VALIDATION_ERROR

    resp = {'code': code}
    if title:
        resp['title'] = title
    if detail:
        resp['detail'] = detail
    if links:
        resp['links'] = links
    if source:
        resp['source'] = source
    if meta:
        resp['meta'] = meta
    return jsonify(
        data={'errors': [resp]},
        status=status,
    )


def success(prepared_obj=None, **kwargs):
    resp = prepared_obj if prepared_obj is not None else kwargs
    return jsonify(
        data={'data': resp},
        status=200,
    )


def last_day_of_month(date=None):
    date = date or datetime.date.today()
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)


def add_or_update_attr(func, param, value):
    assert 'dict' in str(type(value))
    try:
        param = getattr(func, param)
        param.update(value)
    except AttributeError:
        setattr(func, param, value)
