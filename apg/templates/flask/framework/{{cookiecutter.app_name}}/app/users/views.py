from datetime import datetime

from flask import Blueprint

from app.common.decorators import auth_required
from app.users.models import User
from app.users.schemas import ADD_USER_SCHEMA, FILTER_USERS_SCHEMA, UPDATE_USER_SCHEMA

from lib.factory import db
from lib.auth import current_user
from lib.swagger import use_kwargs
from lib.utils import success


mod = Blueprint('users', __name__, url_prefix='/users')


@mod.before_request
@auth_required
def before_request():
    pass


@mod.route('/current/')
def current_user_view():
    """
    Get current user
    :return: user instance
    """
    return success(**current_user.to_dict())


@mod.route('/')
@use_kwargs(FILTER_USERS_SCHEMA)
def list_view(page, limit, sort_by):
    """
    Get list of users
    :param page: number of pages
    :type page: int
    :param limit: result limit
    :type limit: int
    :param sort_by: criterion
    :type sort_by: string
    :return: list of users and number of users
    """
    q = User.query
    total = q.count()

    if sort_by.startswith('-'):
        sort_by = getattr(User, sort_by[1:]).desc()
    else:
        sort_by = getattr(User, sort_by)

    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(
        results=[user.to_dict() for user in q],
        total=total
    )


@mod.route('/<int:user_id>/')
def user_by_id_view(user_id):
    """
    Get certain user
    :param user_id: user identifier
    :type user_id: int
    :return: user instance
    """
    user = User.query.get_or_404(user_id)
    return success(**user.to_dict())


@mod.route('/', methods=['POST'])
@use_kwargs(ADD_USER_SCHEMA)
def add_user_view(**kwargs):
    """
    Create user
    :param name: user name
    :type name: string
    :param password: user password
    :type password: string
    :return: user instance
    """
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return success(**user.to_dict())


@mod.route('/<int:user_id>/', methods=['PUT'])
@use_kwargs(UPDATE_USER_SCHEMA)
def update_user_view(user_id, **kwargs):
    """
    Update user
    :param user_id: user identifier
    :type user_id: int
    :param name: user name
    :type name: string
    :param password: user password
    :type password: string
    :return: user instance
    """
    user = User.query.get_or_404(user_id)
    if not kwargs['name'] and not kwargs['password']:
        return success(), 204

    if kwargs['name']:
        user.name = kwargs['name']

    if kwargs['password']:
        user.password = kwargs['password']

    user.updated_at = datetime.utcnow()
    db.session.commit()

    return success(**user.to_dict())


@mod.route('/<int:user_id>/', methods=['DELETE'])
def delete_user_view(user_id):
    """
    Remove certain user
    :param user_id: user identifier
    :type user_id: int
    :return: user instance
    """
    user = User.query.get_or_404(user_id)
    resp = user.to_dict()
    db.session.delete(user)
    db.session.commit()
    return success(**resp)
