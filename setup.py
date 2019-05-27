from setuptools import setup


setup(
    name='apg',
    version='0.3',
    py_modules=['apg'],
    install_requires=[
        'Click',
        'PyYAML',
        'cookiecutter'
    ],
    entry_points='''
        [console_scripts]
        apg=apg.run:cli
    ''',
)