from app.common.specs import success_response_schema


USER_MODEL_NAME = 'User'


models = {
    USER_MODEL_NAME: {
        'id': int,
        'name': str,
        'created_at': str,
        'updated_at': str,
    },
}

current_user_view = dict(
    summary='Current user',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='get current user',
            resp=USER_MODEL_NAME,
        )
    }
)

list_view = dict(
    summary='Users list',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Get filtered list of user',
            resp=USER_MODEL_NAME,
            is_list=True
        )
    }
)

user_by_id_view = dict(
    summary='User by ID',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Get user by id',
            resp=USER_MODEL_NAME,
        )
    }
)

add_user_view = dict(
    summary='Add user',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Add user',
            resp=USER_MODEL_NAME,
        )
    }
)

update_user_view = dict(
    summary='Update user',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Update user',
            resp=USER_MODEL_NAME,
        )
    }
)

delete_user_view = dict(
    summary='Delete user',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Delete user',
            resp=USER_MODEL_NAME,
        )
    }
)
