import asyncio
import logging

import aiohttp
from aiohttp import web
import click
import uvloop

import config
{% if cookiecutter.use_database == 'y' %}from lib.database import init_db{% endif %}
from lib.swagger import init_docs
from lib.utils import add_routes


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def close_session(app):
    session = app['client_session']
    await session.close()


async def create_app(loop=None, session=None):
    app = web.Application(
        loop=loop,
        debug=config.DEBUG
    )
    if not session:
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            loop=loop
        )
    app['client_session'] = session
    add_routes(app)
    init_docs(app, title='{{cookiecutter.app_name}} API', version='{{cookiecutter.version}}')
    {% if cookiecutter.use_database == 'y' %}await init_db(app){% endif %}
    app.on_cleanup.append(close_session)
    app.router.add_get('/healthz', lambda r: web.Response(text='OK'))
    return app


@click.command()
@click.option('--port', '-p', default=8080)
def run(port):
    if config.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app(loop))
    web.run_app(app, port=port)


if __name__ == '__main__':
    run()  # noqa
