from webargs import fields, validate

from app.common.schemas import FILTER_SCHEMA


FILTER_USERS_SCHEMA = {
    **FILTER_SCHEMA
}

ADD_USER_SCHEMA = {
    'name': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, validate=validate.Length(min=1), description='Password'),
}

UPDATE_USER_SCHEMA = {
    'name': fields.String(missing=None, description='Username'),
    'password': fields.String(missing=None, description='Password'),
}
