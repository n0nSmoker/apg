import importlib
import os

import click
from IPython import embed

from lib.utils import RouteTableDef
{%- if cookiecutter.use_database == 'y' %}
import subprocess
from config import POSTGRES_URI
{% endif %}

@click.group()
def cli():
    pass


@cli.command()
def run_shell():
    import re # noqa
    import os # noqa
    from pprintpp import pprint as p # noqa

    shell_context = locals()
    shell_context.update({})  # add additional context here

    embed(user_ns=shell_context, using=None)

{% if cookiecutter.use_database == 'y' %}
@cli.command()
def dbshell():
    subprocess.call(['pgcli', POSTGRES_URI])
{% endif %}

@cli.command()
def check_apispec():
    errors = []

    dirs = (d for d in os.listdir('app') if not d.startswith('_'))
    for dir_name in dirs:
        try:
            views = importlib.import_module(f'app.{dir_name}.views')
        except ModuleNotFoundError:
            continue

        try:
            specs = importlib.import_module(f'app.{dir_name}.specs')
        except ModuleNotFoundError:
            errors.append(f'Module app.{dir_name} does not contains specification file')
            continue

        route_tables = [v for v in views.__dict__.values() if isinstance(v, RouteTableDef)]
        route_names = {r.handler.__name__ for rt in route_tables for r in rt}
        spec_names = {k for k in specs.__dict__.keys() if not k.startswith('_')}

        missed_routes = route_names - spec_names
        if missed_routes:
            errors.append(f'Module app.{dir_name} specification file missing {missed_routes} routes')

    assert not errors, 'Check is failed! \nErrors:\n%s\n' % '\n'.join(errors)
    print('Check is passed!')


if __name__ == '__main__':
    cli()
