import click


def validate_name(value):
    _ = value.replace('_', '')  # Replace underscores in order to use alnum func
    if not (_.isalnum() and _.islower()):
        raise click.BadParameter('should consist of any lowercase letters + digits/underscores')
    if value[0].isdigit():
        raise click.BadParameter('can not start with digit')
    return value
