# APG
Code generation tool, which helps you to start a project without pain

## Installation
```
pip install apg
```

## Usage
Create new project in current directory (flask/aiohttp/ReactJS)
```bash
$ apg init <framework_name>
```
Add new module to the current project (in current directory)
```bash
$ apg module <name>
```


# Run on local machine
```bash
$ make dev
```

# Tests
To run tests and see tests coverage report just type the following command
```
make test
```

# Documentation
After you started the project all documentation will be available is Swagger format

- Flask - http://127.0.0.1:5000/api/doc/
- aiohttp - http://127.0.0.1:8080/api/doc/
