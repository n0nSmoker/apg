import os
import shutil

module = os.getcwd()
sub_apps = os.path.abspath(os.path.join(module, os.pardir))
app_root = os.path.abspath(os.path.join(sub_apps, os.pardir))
tests = os.path.join(app_root, 'tests')

for item in os.listdir(module):
    if 'test_' in item:
        src_file_path = os.path.join(module, item)
        dst_file_path = os.path.join(tests, item)
        if os.path.isfile(src_file_path):
            shutil.move(src_file_path, dst_file_path)
