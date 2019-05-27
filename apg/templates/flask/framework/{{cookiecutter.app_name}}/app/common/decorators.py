{% if cookiecutter.use_jwt_authorization == 'y' -%}
from functools import wraps

from lib.auth import current_user
from lib.utils import add_or_update_attr, fail


def auth_required(fn):
    """
    decorate view if need authenticated access

    @auth_required
    def some_view():
        ...

    or use it with before_request decorator to enable auth for whole module

    @mod.before_request
    @auth_required
    def before_request():
        pass

    :param fn:
    :return:
    """
    add_or_update_attr(fn, '_swagger', {'auth_required': True})

    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not current_user:
            return fail(title='Access denied', status=403)

        return fn(*args, **kwargs)

    return wrapped
{% endif %}