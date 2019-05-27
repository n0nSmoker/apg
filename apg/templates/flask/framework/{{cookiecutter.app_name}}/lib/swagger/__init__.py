from typing import Callable
from os.path import abspath, dirname, join
from flask import Flask, Blueprint
from marshmallow import validate

from .docs import doc_index, spec_index, generate_spec
from .parser import use_args, use_kwargs, fields


BASE = abspath(dirname(__file__))
STATIC_PATH = join(BASE, 'static')


def init_docs(app: Flask, title: str, version: str, base_url: str = '/api/doc',
              routes_wrapper: Callable = lambda fn: fn):

    docs_bp = Blueprint(
        name='apidocs',
        import_name=__name__,
        static_url_path=base_url,
        static_folder=STATIC_PATH
    )

    # set routes
    spec_url = f'{base_url}/spec.json'
    docs_bp.add_url_rule(f'{base_url}/', 'doc_index', routes_wrapper(doc_index))
    docs_bp.add_url_rule(spec_url, 'spec_index', routes_wrapper(spec_index))

    app.register_blueprint(docs_bp)

    app.docs = {
        'spec_url': spec_url,
        'spec': generate_spec(app, title, version)
    }


__all__ = ('init_docs', 'validate', 'use_args', 'use_kwargs', 'fields')
