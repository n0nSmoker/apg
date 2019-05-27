def success_response_schema(description, resp=None, is_list=False):
    data = {
        'type': 'object'
    }

    if resp:
        if isinstance(resp, str):
            data['$ref'] = f'#/definitions/{resp}'
        else:
            data = resp

    if is_list:
        data = {
            'type': 'object',
            'properties': {
                'results': {
                    'type': 'array',
                    'items': data
                },
                'total': {
                    'type': 'integer'
                }
            }
        }

    return {
        'description': description,
        'schema': {
            'type': 'object',
            'properties': {
                'data': data
            }
        }
    }

{% if cookiecutter.use_jwt_authorization == 'y' -%}
login_view = dict(
    summary='Authorization by login and password',
    tags=['Auth'],
    responses={
        '200': success_response_schema(
            description='Auth token',
            resp={
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                    },
                },
            },
        )
    }
)
{% endif %}