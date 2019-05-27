from datetime import datetime

from app.{{cookiecutter.module_name|lower}}s.models import {{cookiecutter.module_name|capitalize}}
import app.{{cookiecutter.module_name|lower}}s.schemas as schemas
from lib.database import count
from lib.utils import fail, RouteTableDef, success
from lib.webforms import use_kwargs


routes = RouteTableDef(url_prefix='/{{cookiecutter.module_name|lower}}s')


@routes.get('/')
@use_kwargs(schemas.FILTER_{{cookiecutter.module_name|upper}}S_SCHEMA)
async def list_view(_, page, limit, sort_by):
    if sort_by.startswith('-'):
        sort_by = getattr({{cookiecutter.module_name|capitalize}}, sort_by[1:]).desc()
    else:
        sort_by = getattr({{cookiecutter.module_name|capitalize}}, sort_by)

    q = await {{cookiecutter.module_name | capitalize}}.query.order_by(sort_by).offset((page -1) * limit).limit(limit).gino.all()
    total = await count({{cookiecutter.module_name | capitalize}})

    return success(
        results=[{{cookiecutter.module_name|lower}}.to_dict() for {{cookiecutter.module_name|lower}} in q],
        total=total
    )


@routes.get(r'/{% raw %}{{% endraw %}{{cookiecutter.module_name|lower}}_id:\d+}/')
async def {{cookiecutter.module_name|lower}}_by_id_view(request):
    {{cookiecutter.module_name|lower}}_id = request.match_info['{{cookiecutter.module_name|lower}}_id']
    {{cookiecutter.module_name|lower}} = await {{cookiecutter.module_name|capitalize}}.get(int({{cookiecutter.module_name|lower}}_id))
    return success(**{{cookiecutter.module_name|lower}}.to_dict())


@routes.post('/')
@use_kwargs(schemas.ADD_{{cookiecutter.module_name|upper}}_SCHEMA)
async def add_{{cookiecutter.module_name|lower}}_view(_, **kwargs):
    {{cookiecutter.module_name|lower}} = await {{cookiecutter.module_name|capitalize}}.create(**kwargs)
    return success(**{{cookiecutter.module_name|lower}}.to_dict())


@routes.put(r'/{% raw %}{{% endraw %}{{cookiecutter.module_name|lower}}_id:\d+}/')
@use_kwargs(schemas.UPDATE_{{cookiecutter.module_name|upper}}_SCHEMA)
async def update_{{cookiecutter.module_name|lower}}_view(request, **kwargs):
    {{cookiecutter.module_name|lower}}_id = request.match_info['{{cookiecutter.module_name|lower}}_id']
    {{cookiecutter.module_name|lower}} = await {{cookiecutter.module_name | capitalize}}.get(int({{cookiecutter.module_name | lower}}_id))
    await {{cookiecutter.module_name | lower}}.update(updated_at=datetime.utcnow(), **kwargs).apply()
    return success(**{{cookiecutter.module_name|lower}}.to_dict())


@routes.delete(r'/{% raw %}{{% endraw %}{{cookiecutter.module_name|lower}}_id:\d+}/')
async def delete_{{cookiecutter.module_name|lower}}_view(request):
    {{cookiecutter.module_name|lower}}_id = request.match_info['{{cookiecutter.module_name|lower}}_id']
    {{cookiecutter.module_name|lower}} = await {{cookiecutter.module_name|capitalize}}.get(int({{cookiecutter.module_name|lower}}_id))
    await {{cookiecutter.module_name|lower}}.delete()
    return success(**{{cookiecutter.module_name|lower}}.to_dict())
