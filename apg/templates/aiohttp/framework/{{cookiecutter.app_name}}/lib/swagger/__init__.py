from datetime import time
import importlib
from functools import wraps
from os.path import abspath, dirname, join
import re
import json
import constants as const
from aiohttp import web

from lib.utils import jsonify
from config import DEBUG


BASE = abspath(dirname(__file__))
TEMPLATES_PATH = join(BASE, 'templates')
STATIC_PATH = join(BASE, 'static')

DEFAULT_RESPONSES = {
    '400': {
        'description': """
            "errors": [
                {
                    "code": "%s",
                    "title": "error short description",
                    "detail": "error full description",
                    "meta": "error meta data"
                }
            ]
        """ % const.VALIDATION_ERROR
    },
    '404': {
        "description": """
            "errors": [
                {
                    "code": "%s",
                    "meta": "error meta data"
                }
            ]
        """ % const.NOT_FOUND
    },
    '500': {
        "description": """
            "errors": [
                {
                    "code": "%s",
                    "meta": "error meta data"
                }
            ]
        """ % const.INTERNAL_ERROR
    }
}

TYPES_MAP = {
    int: {'type': 'integer'},
    str: {'type': 'string'},
    time: {
        'type': 'string',
        'example': '10:00',
    },
    bool: {'type': 'boolean'},
}


async def doc_index(request):
    """ return doc index.html """
    with open(join(TEMPLATES_PATH, "index.html"), "r") as f:
        text = f.read() % dict(spec_url=request.app["DOC_SPEC_URL"])
        return web.Response(text=text, content_type="text/html", headers={'Server': ''})


async def spec_index(request):
    """ return doc spec """
    return jsonify(request.app["DOC_SPEC"])


def make_ref(model_name: str) -> dict:
    return {'$ref': f'#/definitions/{model_name}'}


def make_response_description(data):
    """
    make pretty formatted description string
    :param data: JSON serializable response object
    :return: description string
    """
    pretty = json.dumps(
        {'data': data},
        ensure_ascii=False,
        sort_keys=True,
        indent=4
    )
    return f'```json\n{pretty}\n```'


def spec_from(specs):
    def decorator(func):
        func.specs_dict = specs

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper

    return decorator


def path_to_params(path, params):
    for arg in re.findall('({([^{}]*:)?([^{}]*)})', path):
        arg_name = arg[2]
        path = path.replace(arg[0], '{%s}' % arg_name)
        params.append({
            'in': 'path',
            'name': arg_name,
            'required': True,
            'type': 'string',
        })
    return path, params


def type2property(type_: any) -> dict:
    if isinstance(type_, str):
        return make_ref(type_)

    if isinstance(type_, list):
        prop = {'type': 'array'}

        if not type_:
            prop['example'] = []
        else:
            el = type_[0]
            prop['items'] = make_ref(el) if isinstance(el, str) else TYPES_MAP[el]

        return prop

    return TYPES_MAP[type_]


def model2definition(model: dict) -> dict:
    return {
        'type': 'object',
        'properties': {k: type2property(v) for k, v in model.items()}
    }


def generate_spec(app, title, version):  # TODO: refactoring in swagger update(too complex) #noqa
    spec = dict(swagger='2.0', info=dict(title=title, version=version), paths={}, definitions={})
    for route in app.router.routes():
        if route.method == 'HEAD':
            continue
        views_mod = route.handler.__module__
        subapp_mod = views_mod.rpartition('.')[0]
        handler_name = route.handler.__name__
        try:
            specs_mod = importlib.import_module(f'{subapp_mod}.specs')
        except ModuleNotFoundError:
            continue

        spec_models = getattr(specs_mod, 'models', None)
        if spec_models:
            spec['definitions'].update({
                k: model2definition(v) for k, v in spec_models.items()
            })

        spec_dict = getattr(specs_mod, handler_name, None)
        if spec_dict is None:
            continue

        if spec_dict.get('debug') and not DEBUG:
            continue

        spec_dict.setdefault('parameters', getattr(route.handler, '_swagger_spec_parameters', []))
        spec_dict.setdefault('responses', {})
        spec_dict['responses'].update(DEFAULT_RESPONSES)

        resource = route.resource
        path = None
        if isinstance(resource, web.PlainResource):
            path = route.resource._path # pylint: disable=W0212
        elif isinstance(resource, web.DynamicResource):
            path = route.resource._formatter # pylint: disable=W0212
        method = route.method.lower()

        path, spec_dict['parameters'] = path_to_params(path, spec_dict['parameters'])

        if path not in spec['paths']:
            spec['paths'][path] = {}
        spec['paths'][path][method] = spec_dict
    return spec


def init_docs(app, title, version, base_url='/api/doc/'):
    # set routes
    spec_url = f'{base_url}spec.json'
    app.router.add_route('GET', base_url, doc_index)
    app.router.add_route('GET', spec_url, spec_index)

    # set static
    app.router.add_static(base_url, STATIC_PATH)

    app["DOC_SPEC_URL"] = spec_url
    app["DOC_SPEC"] = generate_spec(app, title, version)
