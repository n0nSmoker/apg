# {{ cookiecutter.full_app_name }}
## {{ cookiecutter.description }}


## Requirements
- [Docker](https://docs.docker.com/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)

Install requirements for your platform (Linux, Mac, Windows)


## Usage

```bash
$ make <command>
```
> May ask superuser rights (for docker)

List of available commads:
- `dev`  build application containers and run with dev server (runs all new db migrations)
- `build` build application containers
- `up` run application in production mode
- `stop` stop application and all its containers
- `db` initialize application database
- `migrate` generate database migration file
- `upgrade` apply latest database migration files
- `bash` open bash shell inside app container
- `shell` run ipython shell inside app container
- `dbshell` run pimped out database shell inside db container
- `redis-cli` run redis shell in redis container
- `test` run tests all tests
- `test file=path/to/tests.py::some_test` run separate dir/module/test


# Module directory structure:
```
my_microservice
├── app
│   └── some_module
│       ├── models.py <---- data models
│       ├── views.py  <---- CRUD functions
│       ├── specs.py  <---- swagger specification
│       └── shema.py  <---- data schemas
└── tests
    └── test_some_module.py  <---- module tests
```
