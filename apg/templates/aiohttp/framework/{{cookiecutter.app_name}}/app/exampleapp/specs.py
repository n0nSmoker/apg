from app.common.specs import success_response_schema


EXAMPLE_MODEL_NAME = 'Example'


models = {
    EXAMPLE_MODEL_NAME: {
        'id': int,
        'created_at': str,
        'updated_at': str,
    },
}

example_view = dict(
    summary='Example of request',
    tags=['example'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp=EXAMPLE_MODEL_NAME
        )
    }
)

example_json_view = dict(
    summary='Example of json body',
    tags=['example'],
    responses={
        '200': success_response_schema(
            description='Example of json body',
            resp=EXAMPLE_MODEL_NAME
        )
    }
)

example_update_view = dict(
    summary='Example of update',
    tags=['example'],
    responses={
        '200': success_response_schema(
            description='Example of update',
            resp=EXAMPLE_MODEL_NAME
        )
    }
)

example_delete_view = dict(
    summary='Example of delete',
    tags=['example'],
    responses={
        '200': success_response_schema(
            description='Example of delete',
            resp=EXAMPLE_MODEL_NAME
        )
    }
)
