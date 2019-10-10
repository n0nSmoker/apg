from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy.types import UserDefinedType


class CUBE(UserDefinedType):
    def get_col_spec(self, **kw):  # noqa
        return "cube"

    def bind_processor(self, dialect):  # noqa
        def process(value):
            if value is not None:
                return ','.join(str(i) for i in value)
            return value

        return process

    def result_processor(self, dialect, coltype):  # noqa
        def process(value):
            if value is not None:
                value = value.strip(')(')
                return [float(v) for v in value.split(',')]
            return value

        return process

    @property
    def python_type(self):
        return list


class Query(BaseQuery):
    def order_by(self, *criterion):
        """apply one or more ORDER BY criterion to the query or
        one or more of (<db.Model subclass>, <str>) tuples
        and return the newly resulting ``Query``

        """
        def compile_criterion(model, sort_by):
            """
            :param model: db.Model
            :param sort_by: str
            :return: criterion
            """
            if sort_by.startswith('-'):
                return getattr(model, sort_by[1:]).desc()
            return getattr(model, sort_by)

        args = []
        for c in criterion:
            if isinstance(c, tuple):
                model, sort_by = c
                is_correct = issubclass(model, Model) and isinstance(sort_by, str)
                assert is_correct, 'Sorting tuple is incorrect. Must be (<db.Model subclass>, <str>)'
                c = compile_criterion(model=model, sort_by=sort_by)
            elif isinstance(c, str):
                primary_mapper = self._primary_entity
                assert primary_mapper, f'No primary entity found, can not apply {c}'
                c = compile_criterion(model=primary_mapper.mapper.entity, sort_by=c)

            args.append(c)
        return super().order_by(*args)
