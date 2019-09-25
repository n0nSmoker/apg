import collections
import functools
import operator

from apispec.ext.marshmallow.openapi import OpenAPIConverter
from flask import abort, jsonify
from marshmallow.orderedset import OrderedSet
from webargs import fields, missing
from webargs.core import dict2schema
from webargs.flaskparser import FlaskParser

from lib.utils import add_or_update_attr


openapi_converter = OpenAPIConverter('2.0')

DEFAULT_LOCATIONS = ('query', 'form', 'json')
FIELD_MAP = {
    fields.Integer: ('integer', 'int32'),
    fields.Number: ('number', None),
    fields.Float: ('number', 'float'),
    fields.Decimal: ('number', None),
    fields.String: ('string', None),
    fields.Boolean: ('boolean', None),
    fields.UUID: ('string', 'uuid'),
    fields.DateTime: ('string', 'date-time'),
    fields.Date: ('string', 'date'),
    fields.Time: ('string', None),
    fields.Email: ('string', 'email'),
    fields.URL: ('string', 'url'),
    fields.Dict: ('object', None),
    # Assume base Field and Raw are strings
    fields.Field: ('string', None),
    fields.Raw: ('string', None),
    fields.List: ('array', None)
}


def format_errors(form_errors: dict) -> dict:
    errors = []
    for k, v in form_errors.items():
        title = ','.join(v)
        errors.append({
            'title': title,
            'detail': f'Field: {k}. Errors: {title}',
            'meta': {'field': k}
        })
    return {'errors': errors}


def field2parameter(field: fields.Field, name: str, default_location: str = 'query') -> dict:
    location = field.metadata.get('location', default_location)
    description = field.metadata.get('description')
    if location == 'headers':
        location = 'header'
    elif location == 'match_info':
        location = 'path'
    elif location in ('files', 'form'):
        location = 'formData'

    parameter = {
        'in': location,
        'name': field.load_from or name,
        'required': field.required,
        'description': description,
        **openapi_converter.field2property(field)
    }

    if isinstance(field, fields.List):
        parameter['collectionFormat'] = 'multi'

    return parameter


def fields2json_parameter(spec_fields: dict) -> dict:
    properties = {}
    for name, field in spec_fields.items():
        properties[name] = {
            'description': field.metadata.get('description'),
            'required': field.required,
            **openapi_converter.field2property(field)
        }
    return {
        "in": "body",
        "name": "body",
        "required": True,
        "schema": {
            "properties": properties
        }
    }


def field2property(field: fields.Field):
    type_, format_ = FIELD_MAP.get(type(field), ('string', None))
    property_ = {'type': type_, 'format': format_}

    if 'doc_default' in field.metadata:
        property_['default'] = field.metadata['doc_default']
    else:
        default = field.missing
        if default is not missing and not callable(default):
            property_['default'] = default

    property_.update(field2choices(field))

    return property_


def field2choices(field: fields.Field):
    attributes = {}

    comparable = [
        validator.comparable for validator in field.validators
        if hasattr(validator, 'comparable')
    ]
    if comparable:
        attributes['enum'] = comparable
    else:
        choices = [
            OrderedSet(validator.choices) for validator in field.validators
            if hasattr(validator, 'choices')
        ]
        if choices:
            attributes['enum'] = list(functools.reduce(operator.and_, choices))

    return attributes


class CustomHTTPParser(FlaskParser):
    def handle_error(self, error, req, schema, error_status_code=None, error_headers=None):  # TODO simplify #noqa
        response = jsonify(**format_errors(error.normalized_messages()))
        response.status_code = 400
        abort(response)

    def use_args(self, argmap, req=None, locations=None, as_kwargs=False, validate=None, error_status_code=None, error_headers=None):  # TODO simplify #noqa
        """Decorator that injects parsed arguments into a view function or method.

        Example usage with Flask: ::

            @app.route('/echo', methods=['get', 'post'])
            @parser.use_args({'name': fields.Str()})
            def greet(args):
                return 'Hello ' + args['name']

        :param argmap: Either a `marshmallow.Schema`, a `dict`
            of argname -> `marshmallow.fields.Field` pairs, or a callable
            which accepts a request and returns a `marshmallow.Schema`.
        :param tuple locations: Where on the request to search for values.
        :param bool as_kwargs: Whether to insert arguments as keyword arguments.
        :param callable validate: Validation function that receives the dictionary
            of parsed arguments. If the function returns ``False``, the parser
            will raise a :exc:`ValidationError`.
        """
        locations = locations or DEFAULT_LOCATIONS
        _location = locations[0]

        request_obj = req
        # Optimization: If argmap is passed as a dictionary, we only need
        # to generate a Schema once
        if isinstance(argmap, collections.Mapping):
            argmap = dict2schema(argmap)()

        json_fields = {}
        spec_parameters = []
        for name, field in argmap.fields.items():
            if _location == 'json' and 'location' not in field.metadata:
                json_fields[name] = field
            else:
                spec_parameters.append(field2parameter(field, name, _location))

        if json_fields:
            spec_parameters.append(fields2json_parameter(json_fields))

        def decorator(func):
            req_ = request_obj
            # func._swagger_spec_parameters = spec_parameters #noqa
            add_or_update_attr(func, '_swagger', {'spec_parameters': spec_parameters})

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                req_obj = req_

                parsed_args = self.parse(argmap, req=req_obj, locations=locations, validate=validate)

                if as_kwargs: #noqa
                    parsed_args.update(kwargs)
                    return func(*args, **parsed_args)
                else:
                    # Add parsed_args after other positional arguments
                    new_args = args + (parsed_args,)
                    return func(*new_args, **kwargs)

            wrapper.__wrapped__ = func
            return wrapper

        return decorator


parser = CustomHTTPParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
