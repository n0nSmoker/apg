from datetime import time
import importlib
from os.path import abspath, dirname, join
import re
import constants as const
from flask import current_app, Flask, jsonify, Response


BASE = abspath(dirname(__file__))

TEMPLATES_PATH = join(BASE, 'templates')

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

{% if cookiecutter.use_jwt_authorization == 'y' %}
AUTH_PARAM = {
    'in': 'header',
    'name': 'X-Auth-Token',
    'required': 'True',
    'type': 'string',
    'description': 'Токен полученный при авторизации'
}
{% endif %}

TYPES_MAP = {
    int: {'type': 'integer'},
    str: {'type': 'string'},
    time: {
        'type': 'string',
        'example': '10:00',
    },
    bool: {'type': 'boolean'},
}


def doc_index() -> Response:
    """ return doc index.html """
    with open(join(TEMPLATES_PATH, "index.html"), "r") as f:
        text = f.read() % dict(spec_url=current_app.docs['spec_url'])
        return Response(text, headers={'Server': ''})


def spec_index() -> Response:
    """ return doc spec """
    return jsonify(**current_app.docs['spec'])


# TODO: use it for response descriptions or remove  # noqa
def make_response_description(data: any) -> str:
    """
    make pretty formatted description string
    :param data: JSON serializable response object
    :return: description string
    """
    pretty = jsonify(
        {'data': data},
        ensure_ascii=False,
        escape_forward_slashes=False,
        sort_keys=True,
        indent=4
    )
    return f'```json\n{pretty}\n```'


def path_to_params(path):
    params = []

    for arg in re.findall('(<([^<>]*:)?([^<>]*)>)', path):
        arg_name = arg[2]
        path = path.replace(arg[0], {% raw %}'{%s}'{% endraw %} % arg_name)
        params.append({
            'in': 'path',
            'name': arg_name,
            'required': True,
            'type': 'string',
        })

    return params, path


{% if cookiecutter.use_jwt_authorization == 'y' -%}
def auth_required(module_name, funcs, spec_params):
    auth_before_request = False
    auth_before_view = False

    if module_name in funcs.keys():
        for func in funcs[module_name]:
            try:
                auth = getattr(func, '_swagger')['auth_required']
                if auth:
                    auth_before_request = True
            except AttributeError:
                continue

    try:
        if spec_params['auth_required']:
            auth_before_view = True
    except KeyError:
        pass

    required = auth_before_request or auth_before_view

    return required
{% endif %}

def make_ref(model_name: str) -> dict:
    return {'$ref': f'#/definitions/{model_name}'}


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


def generate_spec(app: Flask, title: str, version: str) -> dict:  # TODO: simplify  # noqa
    with app.app_context():
        spec = dict(swagger='2.0', info=dict(title=title, version=version), paths={}, definitions={})
        for rule in current_app.url_map.iter_rules():
            handler = current_app.view_functions[rule.endpoint]
            views_mod = handler.__module__
            app_mod = views_mod.rpartition('.')[0]

            # skip run.py specified handlers
            if not app_mod:
                continue

            try:
                specs_mod = importlib.import_module(f'{app_mod}.specs')
            except ModuleNotFoundError:
                continue

            spec_models = getattr(specs_mod, 'models', None)
            if spec_models:
                spec['definitions'].update({
                    k: model2definition(v) for k, v in spec_models.items()
                })

            spec_dict = getattr(specs_mod, handler.__name__, None)
            if spec_dict is None:
                continue

            if spec_dict.get('debug') and not app.debug:
                continue

            spec_params = getattr(handler, '_swagger', {})

            try:
                spec_dict.setdefault('parameters', spec_params['spec_parameters'])
            except KeyError:
                spec_dict.setdefault('parameters', [])

            spec_dict.setdefault('responses', {})
            spec_dict['responses'].update(DEFAULT_RESPONSES)

            methods = rule.methods - {'HEAD', 'OPTIONS'}
            if not methods:
                continue

            path = rule.rule
            method = next(iter(methods)).lower()
            {% if cookiecutter.use_jwt_authorization == 'y' -%}
            module_name = rule.endpoint.split('.')[0]
            funcs = current_app.before_request_funcs
            if auth_required(module_name, funcs, spec_params):
                spec_dict['parameters'].append(AUTH_PARAM)
            {% endif %}
            path_params, path = path_to_params(path)
            spec_dict['parameters'] += path_params

            if path not in spec['paths']:
                spec['paths'][path] = {}

            spec['paths'][path][method] = spec_dict
        return spec
