import os

import click
import json

import yaml
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter


package_dir = os.path.dirname(os.path.abspath(__file__))
work_dir = os.getcwd()
app_dir = os.path.join(work_dir, 'app')

templates_dir = os.path.join(package_dir, 'templates')

FRAMEWORKS = ('flask', 'aiohttp', 'react')

INFO_FILE_NAME = '.info'


def add_info_file(project_name, **kwargs):
    path = os.path.join(work_dir, project_name, INFO_FILE_NAME)
    with open(path, mode='w+') as stream:
        try:
            yaml.safe_dump(kwargs, stream=stream)
        except yaml.YAMLError as exc:
            click.ClickException(f'Can not create the version file:{path} error:{exc}')


def _get_project_info(path):
    f"""
    Returns general info (version, framework, etc)
    Gets this information from {INFO_FILE_NAME} which should be in yaml format
    :param path:
    :return: dict
    """
    path = os.path.join(path, INFO_FILE_NAME)
    try:
        with open(path) as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        click.ClickException(f'Can not read the version file:{path} error:{exc}')


def _get_framework_name(path):
    """
    Determine framework name
    :param path:
    :return:
    """
    info = _get_project_info(path)
    try:
        return info['framework']
    except KeyError:
        click.ClickException(f'Can not find framework field in info file {os.path.join(path, INFO_FILE_NAME)}')


def _get_framework_dir(name):
    """
    Compose path to framework template
    :param name:
    :return:
    """
    return os.path.join(templates_dir, name, 'framework')


def _get_module_dir(framework):
    """
    Compose path to module template
    :param framework:
    :return:
    """
    return os.path.join(templates_dir, framework, 'module')


def _get_framework_context(name):
    """
    Loads context for framework template
    :param name:
    :return:
    """
    path = _get_framework_dir(name)
    return _get_context(path)


def _get_module_context(framework):
    """
    Loads context for module template
    :param framework:
    :return:
    """
    path = _get_module_dir(framework)
    return _get_context(path)


def _get_context(path):
    """
    Loads context from given path
    :param path:
    :return:
    """
    path = os.path.join(path, 'cookiecutter.json')
    f = open(path)
    return json.loads(f.read())


def _update_context(context, skip=()):
    """
    Update context, prompting user questions
    :param context:
    :param skip:
    :return:
    """
    keys_to_ask = {k for k in context.keys() - set(skip) if not k.startswith('_')}
    if keys_to_ask:
        click.echo("Please answer the questions below (default value in square brackets)")
    for k in keys_to_ask:
        context[k] = input(f'{k} [{context[k]}]: ') or context[k]
    return context


def new_project(name, framework):
    """
    Creates new project in current work directory
    :param name:
    :param framework:
    :return:
    """
    context = _get_framework_context(framework)
    context['app_name'] = name
    context = _update_context(
        context=context,
        skip=('app_name', 'full_app_name', 'description', 'version')
    )

    framework_dir = _get_framework_dir(framework)
    cookiecutter(
        template=framework_dir,
        output_dir=work_dir,
        extra_context=context,
        no_input=True
    )
    add_info_file(project_name=name, framework=framework, version=context['version'])
    click.echo(
        f'Project name:{name} framework:{framework} is created in {work_dir}'
    )


def new_module(name):
    """
    Adds new module to current app directory
    :param name:
    :return:
    """
    if not (os.path.isdir(app_dir) and os.path.exists(app_dir)):
        raise click.ClickException(
            f'Can not find application folder {app_dir}'
        )
    framework = _get_framework_name(work_dir)

    context = _get_module_context(framework)
    context['module_name'] = name

    module_dir = _get_module_dir(framework)
    try:
        cookiecutter(
            template=module_dir,
            output_dir=app_dir,
            extra_context=context,
            no_input=True
        )
    except OutputDirExistsException:
        click.ClickException(f'Module {name} already exists in {app_dir}')

    click.echo(f'New module {name} is created in {app_dir}')

