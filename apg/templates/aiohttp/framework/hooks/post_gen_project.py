import os
import shutil

# remove database worker files if not use
if '{{cookiecutter.use_database}}' == 'n':
    database_py_path = os.path.join(os.getcwd(), 'lib/database.py')
    os.remove(database_py_path)

    migrations_path = os.path.join(os.getcwd(), 'migrations')
    shutil.rmtree(migrations_path)

    alembic_ini_path = os.path.join(os.getcwd(), 'alembic.ini')
    os.remove(alembic_ini_path)
