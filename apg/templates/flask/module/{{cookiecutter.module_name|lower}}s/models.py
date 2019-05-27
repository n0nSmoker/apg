from datetime import datetime

from lib.factory import db
from sqlalchemy_serializer import SerializerMixin


class {{cookiecutter.module_name|capitalize}}(db.Model, SerializerMixin):
    __tablename__ = '{{cookiecutter.module_name|lower}}s'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
