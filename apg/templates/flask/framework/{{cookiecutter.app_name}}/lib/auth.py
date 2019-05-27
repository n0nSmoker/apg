import base64
from datetime import datetime, timedelta
import hashlib
import hmac
from typing import Callable

import bcrypt
from flask import _request_ctx_stack, current_app, Flask, request
import jwt
from werkzeug.local import LocalProxy


DEFAULTS = {
    'JWT_EXPIRE_HOURS': 8,
    'JWT_ISSUER': 'jwt_auth',
    'JWT_KEY': 'jwt_auth_secret_key',
    'JWT_ALGORITHM': 'HS256',
    'JWT_COOKIE_NAME': 'JAT',
    'JWT_HEADER_NAME': 'X-Auth-Token',
    'PASSWORD_SALT': 'x5_app_pwd_salt)(*&^%$#@!'
}


def encode(string):
    if isinstance(string, str):
        return bytes(string, 'utf-8')

    return string


class AuthManager:
    def __init__(self, app: Flask, load_user: Callable[[int], dict]):
        app.auth_manager = self
        self._load_user = load_user
        self.jwt_expire = app.config.get('JWT_EXPIRE_HOURS')
        self.jwt_issuer = app.config.get('JWT_ISSUER')
        self.jwt_key = app.config.get('JWT_KEY')
        self.jwt_algorithm = app.config.get('JWT_ALGORITHM')
        self.jwt_cookie_name = app.config.get('JWT_COOKIE_NAME')
        self.jwt_header_name = app.config.get('JWT_HEADER_NAME')
        self.password_salt = app.config.get('PASSWORD_SALT')

    def get_access_token(self, user_id: int) -> dict:
        return jwt.encode(
            payload={
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(hours=self.jwt_expire),
                'iss': self.jwt_issuer
            },
            key=self.jwt_key,
            algorithm=self.jwt_algorithm
        ).decode('utf-8')

    def decode_token(self, token: str) -> dict:
        return jwt.decode(
            jwt=token,
            key=self.jwt_key,
            issuer=self.jwt_issuer,
            algorithms=[self.jwt_algorithm]
        )

    def get_user(self):
        if not hasattr(_request_ctx_stack.top, 'user'):
            user = None
            access_token = request.cookies.get(self.jwt_cookie_name, request.headers.get(self.jwt_header_name))

            if access_token:
                try:
                    token_data = self.decode_token(access_token)
                    user = self._load_user(token_data['user_id'])
                except jwt.InvalidTokenError:
                    pass

            _request_ctx_stack.top.user = user

        return _request_ctx_stack.top.user

    # hashing password
    def get_hmac(self, password: str) -> bytes:
        h = hmac.new(
            key=encode(self.password_salt),
            msg=encode(password),
            digestmod=hashlib.sha512
        )
        return base64.b64encode(h.digest())

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(self.get_hmac(password), salt=bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(self.get_hmac(password), encode(hashed_password))


current_user = LocalProxy(lambda: current_app.auth_manager.get_user())  # pylint: disable=unnecessary-lambda
get_access_token = LocalProxy(lambda: current_app.auth_manager.get_access_token)
hash_password = LocalProxy(lambda: current_app.auth_manager.hash_password)
verify_password = LocalProxy(lambda: current_app.auth_manager.verify_password)
