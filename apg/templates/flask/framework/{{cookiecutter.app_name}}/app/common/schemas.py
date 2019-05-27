from webargs import fields, validate


FILTER_SCHEMA = {
    'page': fields.Int(missing=1),
    'limit': fields.Int(missing=10),
    'sort_by': fields.Str(validate=validate.OneOf(['id', 'created_at', 'updated_at']), missing='created_at')
}
