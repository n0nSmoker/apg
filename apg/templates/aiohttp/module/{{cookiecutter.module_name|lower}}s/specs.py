from app.common.specs import success_response_schema


{{cookiecutter.module_name|upper}}_MODEL_NAME = '{{cookiecutter.module_name|capitalize}}'


models = {
    {{cookiecutter.module_name|upper}}_MODEL_NAME: {
        'id': int,
        'created_at': str,
        'updated_at': str,
    },
}

list_view = dict(
    summary='{{cookiecutter.module_name|capitalize}} list',
    tags=['{{cookiecutter.module_name|upper}}S'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp={{cookiecutter.module_name|upper}}_MODEL_NAME,
            is_list=True
        )
    }
)

{{cookiecutter.module_name|lower}}_by_id_view = dict(
    summary='{{cookiecutter.module_name|capitalize}} by id',
    tags=['{{cookiecutter.module_name|upper}}S'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp={{cookiecutter.module_name|upper}}_MODEL_NAME
        )
    }
)

add_{{cookiecutter.module_name|lower}}_view = dict(
    summary='{{cookiecutter.module_name|capitalize}} create',
    tags=['{{cookiecutter.module_name|upper}}S'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp={{cookiecutter.module_name|upper}}_MODEL_NAME
        )
    }
)

update_{{cookiecutter.module_name|lower}}_view = dict(
    summary='{{cookiecutter.module_name|capitalize}} update',
    tags=['{{cookiecutter.module_name|upper}}S'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp={{cookiecutter.module_name|upper}}_MODEL_NAME
        )
    }
)

delete_{{cookiecutter.module_name|lower}}_view = dict(
    summary='{{cookiecutter.module_name|capitalize}} by id',
    tags=['{{cookiecutter.module_name|upper}}S'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp={{cookiecutter.module_name|upper}}_MODEL_NAME
        )
    }
)
