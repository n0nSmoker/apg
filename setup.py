from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='apg',
    version='0.4.8',
    description='Awesome project generation tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
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
