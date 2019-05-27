import os
import shutil

# remove auth if not use
if '{{cookiecutter.use_jwt_authorization}}' == 'n':
    auth_lib_path = os.path.join(os.getcwd(), 'lib/auth.py')
    os.remove(auth_lib_path)

    users_module_path = os.path.join(os.getcwd(), 'app/users')
    shutil.rmtree(users_module_path)

    test_users_path = os.path.join(os.getcwd(), 'tests/test_users.py')
    os.remove(test_users_path)
