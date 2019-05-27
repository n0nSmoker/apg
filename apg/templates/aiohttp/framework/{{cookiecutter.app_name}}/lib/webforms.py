import collections
import functools
import json

from aiohttp.web_exceptions import HTTPBadRequest, HTTPUnauthorized
from apispec.ext.marshmallow.openapi import OpenAPIConverter
from webargs import fields
from webargs.aiohttpparser import AIOHTTPParser
from webargs.core import dict2schema

from constants import VALIDATION_ERROR


openapi_converter = OpenAPIConverter('2.0')

# Error Example
# {
#     “errors”: [
#         {
#             “code”: “some.error.code”,
#             “status”: “400”,
#             “title”: “короткий текст ошибки”,
#             “detail”: “расширенное описание ошибки”,
#             “links”: {
#                 “about”: “https://some.url/describing/error”
#             },
#             “source”: {
#                 “pointer”: “/data/path/to/attribute”,
#                 “parameter”: “uri_param_name”
#             },
#             “meta”: {
#                 произвольные данные, связанные с ошибкой
#             }
#         }
#     ]
# }


DEFAULT_LOCATIONS = ('query', 'form', 'json')


def format_errors(form_errors):
    errors = []
    for k, v in form_errors.items():
        title = ','.join(v)
        errors.append(dict(
            code=VALIDATION_ERROR,
            title=title,
            detail=f'Field: {k}. Errors: {title}',
            meta=dict(field=k)
        ))
    return json.dumps(dict(errors=errors))


def field2parameter(field, name, default_location='query'):
    location = field.metadata.get('location', default_location)
    if location == 'headers':
        location = 'header'
    elif location == 'match_info':
        location = 'path'

    parameter = {
        'in': location,
        'name': field.load_from or name,
        'required': field.required,
        **openapi_converter.field2property(field)
    }

    if isinstance(field, fields.List):
        parameter['collectionFormat'] = 'multi'

    return parameter


def fields2json_parameter(spec_fields):
    properties = {}
    for name, field in spec_fields.items():
        properties[name] = {
            'description': field.metadata.get('description'),
            'required': field.required,
        }
        properties[name].update(openapi_converter.field2property(field))
    return {
        "in": "body",
        "name": "body",
        "required": True,
        "schema": {
            "properties": properties
        }
    }


class CustomHTTPParser(AIOHTTPParser):
    def handle_error(
            self,
            error,
            req,
            schema,
            error_status_code=None,
            error_headers=None
    ):
        if error_status_code == 401:
            raise HTTPUnauthorized()

        raise HTTPBadRequest(
            body=format_errors(error.messages).encode('utf-8'),
            content_type='application/json'
        )

    def parse_files(self, req, name, field):
        raise NotImplementedError(
            "parse_files is not implemented. You may be able to use parse_form for "
            "parsing upload data."
        )

    def use_args(self, argmap, req=None, locations=None, as_kwargs=False,       # noqa
                 validate=None, error_status_code=None, error_headers=None):
        """Decorator that injects parsed arguments into a view function or method.

        Example usage: ::

            @routes.<method>('/echo')
            @parser.use_args({'name': fields.Str()})
            async def greet(args):
                return 'Hello ' + args['name']

        :param argmap: Either a `marshmallow.Schema`, a `dict`
            of argname -> `marshmallow.fields.Field` pairs, or a callable
            which accepts a request and returns a `marshmallow.Schema`.
        :param req: request object.
        :param tuple locations: Where on the request to search for values.
        :param bool as_kwargs: Whether to insert arguments as keyword arguments.
        :param callable validate: Validation function that receives the dictionary
            of parsed arguments. If the function returns ``False``, the parser
            will raise a :exc:`ValidationError`.
        :param error_status_code: error status code.
        :param error_headers: error headers.
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
            func._swagger_spec_parameters = spec_parameters # TODO must fix in swagger update #noqa
            # add_or_update_attr(func, '_swagger', {'spec_parameters': spec_parameters})

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                req_obj = req_

                # if as_kwargs is passed, must include all args
                # force_all = as_kwargs

                if not req_obj:
                    req_obj = self.get_request_from_view_args(func, args, kwargs)
                # NOTE: At this point, argmap may be a Schema, or a callable

                parsed_args = await self.parse(argmap, req=req_obj, locations=locations, validate=validate)

                if as_kwargs: # TODO must fix in swagger update #noqa
                    parsed_args.update(kwargs)
                    return await func(*args, **parsed_args)
                else:
                    # Add parsed_args after other positional arguments
                    new_args = args + (parsed_args, )
                    return await func(*new_args, **kwargs)
            wrapper.__wrapped__ = func
            return wrapper

        return decorator


parser = CustomHTTPParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
