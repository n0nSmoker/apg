from setuptools import setup


setup(
    name='apg',
    version='0.4.5',
    description='Awesome project generation tool',
    author='Y-Bro',
    url='https://github.com/n0nSmoker/apg',
    keywords=['apg', 'generate project', 'framework', 'cookie-cutter'],
    packages=['apg', 'apg.utils'],
    py_modules=['apg', 'apg.utils'],
    include_package_data=True,
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
