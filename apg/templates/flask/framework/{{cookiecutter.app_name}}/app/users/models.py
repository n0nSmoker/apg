from datetime import datetime

from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from lib.factory import db
from lib.auth import hash_password


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-password',)

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @validates('password')
    def encrypt_pwd(self, _, pwd):  # noqa
        return hash_password(pwd) if pwd else None
