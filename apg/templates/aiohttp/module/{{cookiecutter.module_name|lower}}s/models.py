from datetime import datetime

from lib.database import db


class {{cookiecutter.module_name|capitalize}}(db.Model):  # noqa
    __tablename__ = '{{cookiecutter.module_name|lower}}s'

    id = db.Column(db.Integer(), primary_key=True)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
