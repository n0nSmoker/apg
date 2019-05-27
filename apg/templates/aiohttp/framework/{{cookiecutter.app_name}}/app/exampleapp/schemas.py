from webargs import fields


EXAMPLE_SCHEMA = {
    'int_field': fields.Int(required=True, description='example description'),
    'str_field': fields.Str(missing=None, description='example description'),
}

EXAMPLE_JSON_SCHEMA = {
    'test_nesting': fields.Nested({
        'int_param': fields.Int(),
        'str_param': fields.Str()
    }, many=True)
}

EXAMPLE_UPDATE_SCHEMA = {
    'int_field': fields.Int(missing=None, description='example description'),
    'str_field': fields.Str(missing=None, description='example description'),
}
