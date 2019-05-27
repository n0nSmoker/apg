import click

from apg.commands import new_project, new_module, FRAMEWORKS
from apg.utils.validators import validate_name


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.argument('framework', type=click.Choice(FRAMEWORKS))
@click.pass_context
def init(ctx, framework):
    name = validate_name(click.prompt('Please enter the project name'))
    new_project(name=name, framework=framework)


@cli.command()
@click.argument('name', callback=lambda ctx, param, value: validate_name(value))
@click.pass_context
def module(ctx, name):
    new_module(name=name)
