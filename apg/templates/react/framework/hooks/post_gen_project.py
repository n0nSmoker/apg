import os
import shutil


app_path = os.getcwd()
dist_path = os.path.join(app_path, '{{cookiecutter.dist_relative_path}}')

if not os.path.exists(dist_path):
    os.makedirs(dist_path)

shutil.move(
    src=os.path.join(app_path, 'index.html'),
    dst=os.path.join(dist_path, 'index.html')
)
