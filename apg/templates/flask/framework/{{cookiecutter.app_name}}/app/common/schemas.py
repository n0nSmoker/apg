from webargs import fields, validate


FILTER_SCHEMA = {
    'page': fields.Int(missing=1, validate=validate.Range(min=1, max=100)),
    'limit': fields.Int(missing=10, validate=validate.Range(min=1, max=1000)),
    'sort_by': fields.Str(validate=validate.OneOf(['id', 'created_at', 'updated_at']), missing='created_at')
}
