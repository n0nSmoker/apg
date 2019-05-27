from flask import current_app as app
from sqlalchemy.dialects.postgresql import insert


def upsert(instance, reread=True):
    """
    Inserts or updates row
    :param instance: SQLAlchemy model instance
    :param reread: bool whether to return upserted instance
    :return: None | SQLAlchemy instance
    """

    model = instance.__class__
    columns = instance.__table__.columns
    unique = {c.name for c in columns if c.unique}
    defaults = {c.name: c.default.arg for c in columns if c.default}
    if not unique:  # or unique_constraints:
        raise Exception('No unique constraints in model, no need in upsert')

    # Get data to update instance
    schema = []
    for c in columns:
        k = '-%s' % c.name if c.primary_key else c.name
        schema.append(k)
    data = instance.to_dict(only=schema)

    # Set default values if needed
    for k, v in defaults.items():
        if data.get(k) is None:
            if callable(v):
                v = v(ctx=app.app_context)
            data[k] = v

    statement = insert(model).values(**data).on_conflict_do_update(
        set_=data,
        index_elements=unique,
    )
    app.db.session.execute(statement)
    app.db.session.commit()
    if reread:
        return model.query.filter_by(**{c: data[c] for c in unique}).one()
