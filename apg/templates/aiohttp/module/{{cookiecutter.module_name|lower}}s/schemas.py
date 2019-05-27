from app.common.schemas import FILTER_SCHEMA


FILTER_{{cookiecutter.module_name|upper}}S_SCHEMA = {
    **FILTER_SCHEMA
}

ADD_{{cookiecutter.module_name|upper}}_SCHEMA = {

}

UPDATE_{{cookiecutter.module_name|upper}}_SCHEMA = {
    **ADD_{{cookiecutter.module_name|upper}}_SCHEMA
}
