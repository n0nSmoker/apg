from flask import Blueprint
{% if cookiecutter.use_jwt_authorization == 'y' -%}
from webargs import fields

from app.users.models import User
from lib.auth import get_access_token, verify_password
from lib.swagger import use_kwargs
from lib.utils import fail, success
{% endif %}

mod = Blueprint('common', __name__)


@mod.route('/')
def root_view():
    return 'Main page'
    
    
@mod.route('/heartbeat/')
def heartbeat_view():
    """Service availability check

    :return: ''
    """
    return ''


{% if cookiecutter.use_jwt_authorization == 'y' -%}
@mod.route('/login/', methods=['POST'])
@use_kwargs({
    'login': fields.Str(required=True),
    'password': fields.Str(required=True),
})
def login_view(login, password):
    """
    User login
    :param login: user login
    :type login: string
    :param password: user password
    :type password: string
    :return: jwt token
    """
    user = User.query.filter_by(name=login).one_or_none()

    if not user:
        return fail(title='User not registered')

    if not verify_password(password=password, hashed_password=user.password):
        return fail(title='Wrong username or password')

    resp = {'access_token': get_access_token(user_id=user.id)}
    return success(resp)
{% endif %}