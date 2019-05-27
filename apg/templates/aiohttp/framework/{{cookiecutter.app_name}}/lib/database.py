import logging
import os

from alembic import command
from alembic.config import Config
import asyncpg
from gino.crud import CRUDModel
from gino.ext.aiohttp import Gino, URL
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy_serializer import SerializerMixin

from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER


class SerializerCRUDModel(SerializerMixin, CRUDModel):
    """ Mixin for integration SQLAlchemy-serializer """

    @property
    def serializable_keys(self):
        """
        :return: set of keys available for serialization
        """
        # look at gino.crud.CRUDModel.to_dict
        cls = self.__class__
        return {cls._column_name_map.invert_get(c.name) for c in cls}  # noqa


db = Gino(model_classes=(SerializerCRUDModel,))


async def count(model, *args):
    """
    Return count of items in query

    Usage with logical operators:

        from sqlalchemy import _and, _or

        count(model, or_(clause1, clause2)

        count(model, and_(or_(clause1, clause2), clause3))

    :param model: selected model
    :param args: filtering clauses
    :return: integer
    """
    query = select([db.func.count(model.id)])
    if args:
        for clause in args:
            query = query.where(clause)
    return await db.scalar(query)


async def get_db_connection():
    return await asyncpg.connect(
        user=POSTGRES_USER,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        password=POSTGRES_PASSWORD
    )


async def is_db_exist():
    conn = await get_db_connection()
    names_q = 'SELECT datname FROM pg_database WHERE datistemplate = false;'
    names = {row[0] for row in await conn.fetch(names_q)}
    await conn.close()
    return POSTGRES_DB in names


async def create_database():
    if not await is_db_exist():
        conn = await get_db_connection()
        await conn.execute(f'CREATE DATABASE {POSTGRES_DB};')
        await conn.close()


async def drop_database():
    if await is_db_exist():
        conn = await get_db_connection()
        await conn.execute(f'DROP DATABASE {POSTGRES_DB};')
        await conn.close()


def upgrade_migrations():
    ini_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'alembic.ini'
    )
    config = Config(ini_path)
    try:
        command.upgrade(config=config, revision='head')
    except DatabaseError as e:
        logging.error('Error on migrations execute\nORIG: %s', e.orig)


async def start_db(app):
    await create_database()
    await db.set_bind(
        bind=URL(
            drivername='asyncpg',
            username=POSTGRES_USER,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB
        ),
        echo=app.debug
    )
    upgrade_migrations()


async def close_db(_):
    await db.pop_bind().close()


async def init_db(app):
    app.on_startup.append(start_db)
    app.on_cleanup.append(close_db)
