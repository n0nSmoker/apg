import inspect
import re

from flask import jsonify
from flask_sqlalchemy import Model
from sqlalchemy.sql.schema import Table
from werkzeug.utils import find_modules, import_string


def get_url_map(app):
    url_map = dict()
    p = re.compile(r'(<[\w]+)|(>)')

    for u in app.url_map.iter_rules():
        route = p.sub('', u.rule)

        if '.' not in u.endpoint:
            url_map[u.endpoint] = route
            continue

        mod, name = u.endpoint.split('.')
        if not url_map.get(mod):
            url_map[mod] = {}
        url_map[mod][name] = route

    return url_map


class ApiException(Exception):
    def __init__(self, message, status=400):
        super().__init__()
        self.message = message
        self.status = status

    def to_result(self):
        return fail(title=self.message, status=self.status)


def find_models_and_tables():
    models_dict = {}
    for module_name in find_modules('app', include_packages=True):
        models_module = import_string('%s.models' % module_name, silent=True)
        if models_module:
            for name, item in models_module.__dict__.items():
                if (inspect.isclass(item) and Model in inspect.getmro(item)) \
                   or item.__class__ is Table:
                    models_dict[name] = item
    return models_dict


def setattrs(obj, **kwargs):
    """ Setting multiple object attributes at once """

    attrs = (a for a in dir(obj) if not a.startswith('_'))
    for attr in attrs:
        if attr in kwargs:
            setattr(obj, attr, kwargs[attr])


def success(prepared_obj=None, **kwargs):
    resp = prepared_obj if prepared_obj is not None else kwargs
    status = 200
    return jsonify(data=dict(**resp)), status


def fail(*, title=None, detail=None, status=400):
    resp = {}
    if title:
        resp['title'] = title
    if detail:
        resp['detail'] = detail
    return jsonify(**resp), status


def add_or_update_attr(func, param, value):
    assert 'dict' in str(type(value))
    try:
        param = getattr(func, param)
        param.update(value)
    except AttributeError:
        setattr(func, param, value)
