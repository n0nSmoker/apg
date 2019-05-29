# APG
Code generation tool, which helps you to start a project without pain

## Dependencies
 - make
 - docker
 - docker-compose
 - cookiecutter
 - Click

for react projects
   - npm 
## Installation
```
pip install apg
```

## Usage
Create new project in current directory

Choose one of available framework
   - flask
   - aiohttp
   - react

```bash
$ apg init <framework_name>
```
Add new module to the current project (in current directory)
> only available at flask and aiohttp
```bash
$ apg module <name>
```


### Run on local machine
```bash
$ make dev # Flask and aiohttp
```

### Bash commands
Flask project:
```bash
$ make dev # build application containers and run in developer mode
$ make build # build application containers
$ make up # run application in prodaction mode
$ make stop # stop application and running containers
$ make db # initialize database
$ make migrate # create data migration for database
$ make bash # run bash shell inside application container
$ make shell # run pimped out python console
$ make dbshell # run databse console
$ make test # run autotests
``` 
Aiohttp project:
```bash
$ make dev # build application containers and run in developer mode
$ make shell # run pimped out python console
$ make check # check apispec
$ make dbshell # run database console
$ make migrate # create data migration for database
$ make upgrade # apply data migrations to database
$ make test # run autotests 
```
React project:
```bash
$ npm start:dev # in standalone project start dev-server, otherwise compile project in dist folder and start watching it
$ npm build:prod # build production
```
### Tests
To run tests and see tests coverage report just type the following command

Flask and Aiohttp:
```bash
$ make test # to test all project files
$ make test file=<folder_name> # to run all test files in folder
$ make test file=<folder_name>/<file_name> # to run all tests in single file
$ make test file=<folder_name>/<file_name>::<test_case_name> # to run sinle test case
```
### Documentation
After you started the project all documentation will be available is Swagger format

- Flask - http://127.0.0.1:5000/api/doc/
- aiohttp - http://127.0.0.1:8080/api/doc/
