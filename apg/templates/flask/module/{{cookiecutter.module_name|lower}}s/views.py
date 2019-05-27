from datetime import datetime

from flask import Blueprint
from lib.factory import db

from lib.swagger import use_kwargs
from lib.utils import setattrs, success

from .models import {{cookiecutter.module_name|capitalize}}
import app.{{cookiecutter.module_name|lower}}s.schemas as schemas

mod = Blueprint('{{cookiecutter.module_name|lower}}s', __name__, url_prefix='/{{cookiecutter.module_name|lower}}s')


@mod.route('/')
@use_kwargs(schemas.FILTER_{{cookiecutter.module_name|upper}}S_SCHEMA)
def list_view(page, limit, sort_by):
    q = {{cookiecutter.module_name|capitalize}}.query
    total = q.count()

    if sort_by.startswith('-'):
        sort_by = getattr({{cookiecutter.module_name|capitalize}}, sort_by[1:]).desc()
    else:
        sort_by = getattr({{cookiecutter.module_name|capitalize}}, sort_by)

    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(
        results=[{{cookiecutter.module_name|lower}}.to_dict() for {{cookiecutter.module_name|lower}} in q],
        total=total
    )


@mod.route('/<int:{{cookiecutter.module_name|lower}}_id>/')
def {{cookiecutter.module_name|lower}}_by_id_view({{cookiecutter.module_name|lower}}_id):
    {{cookiecutter.module_name|lower}} = {{cookiecutter.module_name|capitalize}}.query.filter_by(id={{cookiecutter.module_name|lower}}_id).one()
    return success(**{{cookiecutter.module_name|lower}}.to_dict())


@mod.route('/', methods=['POST'])
@use_kwargs(schemas.ADD_{{cookiecutter.module_name|upper}}_SCHEMA)
def add_{{cookiecutter.module_name|lower}}_view({{cookiecutter.module_name|lower}}_id=None, **kwargs):
    if {{cookiecutter.module_name|lower}}_id:
        {{cookiecutter.module_name | lower}} = {{cookiecutter.module_name|capitalize}}.query.filter_by(id={{cookiecutter.module_name|lower}}_id).one()
        setattrs({{cookiecutter.module_name|lower}}, **kwargs, updated_at=datetime.utcnow())
    else:
        {{cookiecutter.module_name | lower}} = {{cookiecutter.module_name|capitalize}}(**kwargs)
        db.session.add({{cookiecutter.module_name|lower}})

    db.session.commit()

    return success(**{{cookiecutter.module_name|lower}}.to_dict())


@mod.route('/<int:{{cookiecutter.module_name|lower}}_id>/', methods=['PUT'])
@use_kwargs(schemas.UPDATE_{{cookiecutter.module_name|upper}}_SCHEMA)
def update_{{cookiecutter.module_name|lower}}_view({{cookiecutter.module_name|lower}}_id, **kwargs):
    return add_{{cookiecutter.module_name|lower}}_view({{cookiecutter.module_name|lower}}_id, **kwargs)


@mod.route('/<int:{{cookiecutter.module_name|lower}}_id>/', methods=['DELETE'])
def delete_{{cookiecutter.module_name|lower}}_view({{cookiecutter.module_name|lower}}_id):
    {{cookiecutter.module_name | lower}} = {{cookiecutter.module_name|capitalize}}.query.filter_by(id={{cookiecutter.module_name|lower}}_id).one()
    db.session.delete({{cookiecutter.module_name|lower}})
    db.session.commit()
    return success(**{{cookiecutter.module_name|lower}}.to_dict())
