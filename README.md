# APG
Code generation tool, which helps you to start a project without pain.

**Contents**
- [Installation](#Installation)
- [Usage](#Usage)

## Installation
```bash
pip install apg
```

**Dependencies**
 - make
 - docker
 - docker-compose
 - cookiecutter
 - Click
 - npm (for ReactJS projects)
  
## Usage
#### Create a new project in the current directory:
```bash
$ apg init <framework_name>
```
**Available frameworks:**
   - ***flask*** ([Flask](http://flask.pocoo.org/) used as basis, we added webargs, Swagger, pytest and other handy stuff)
   - ***aiohttp*** ([AIOHTTP](http://flask.pocoo.org/) used as basis, but we completely reorganized it to look more like flask. Also added Swagger, webargs and so on)
   - ***react*** (Only basic functionality of ReactJS application)

Once you've done that, commands listed below will be available

**Flask project:**
```bash
$ make dev # build application containers and run in developer mode
$ make build # build application containers
$ make up # run application in production mode
$ make stop # stop application and running containers
$ make db # initialize database
$ make migrate # create data migration for database
$ make bash # run bash shell inside application container
$ make shell # run pimped out python console
$ make dbshell # run databse console
$ make test # run autotests (all project files)
$ make test file=<folder_name> # to run all test files in folder
$ make test file=<folder_name>/<file_name> # to run all tests in single file
$ make test file=<folder_name>/<file_name>::<test_case_name> # to run single test case
```

**AIOHTTP project:**
```bash
$ make dev # build application containers and run in developer mode
$ make shell # run pimped out python console
$ make check # check apispec
$ make dbshell # run database console
$ make migrate # create data migration for database
$ make upgrade # apply data migrations to database
$ make test # run autotests (all project files)
$ make test file=<folder_name> # to run all test files in folder
$ make test file=<folder_name>/<file_name> # to run all tests in single file
$ make test file=<folder_name>/<file_name>::<test_case_name> # to run single test case
```

> After you run `make dev` command 
>The API documentation will be available (SwaggerUI)
> - Flask - http://127.0.0.1:5000/api/doc/
> - aiohttp - http://127.0.0.1:8080/api/doc/

**React project:**
```bash
$ npm start:dev # in standalone project start dev-server, otherwise compile project in dist folder and start watching it
$ npm build:prod # build production
```

#### Add a new module to the current project (current directory):
```bash
$ apg module <name>
```

