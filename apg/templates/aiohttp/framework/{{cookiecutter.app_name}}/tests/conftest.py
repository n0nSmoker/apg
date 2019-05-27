import aiohttp
import pytest
from yarl import URL

from config import EXAMPLE_API_DOMAIN
{% if cookiecutter.use_database == 'y' %}from lib.database import drop_database{% endif %}
from run import create_app

from .fake_api import FakeExampleAPI, FakeResolver


FAKE_API_URLS = {
    FakeExampleAPI: EXAMPLE_API_DOMAIN
}


async def start_fake_apis(loop):
    fake_apis_info = {}
    fake_apis = [
        api_cls(loop=loop, host=URL(url).host) for api_cls, url in FAKE_API_URLS.items()
    ]
    for fake_api in fake_apis:
        fake_api_info = await fake_api.start()
        fake_apis_info[fake_api] = fake_api_info
    return fake_apis_info


async def stop_fake_apis(fake_apis):
    for fake_api in fake_apis:
        await fake_api.stop()


@pytest.fixture
def test_app(loop):
    fake_apis = loop.run_until_complete(start_fake_apis(loop))
    resolver_info = {}
    for fake_api, info in fake_apis.items():  # noqa
        resolver_info.update(info)
    resolver = FakeResolver(resolver_info, loop=loop)
    connector = aiohttp.TCPConnector(loop=loop, resolver=resolver, verify_ssl=False)
    session = aiohttp.ClientSession(connector=connector, loop=loop)

    app = loop.run_until_complete(create_app(loop=loop, session=session))

    async def teardown(_):
        await stop_fake_apis(fake_apis)
        {% if cookiecutter.use_database == 'y' %}await drop_database(){% endif %}

    app.on_cleanup.append(teardown)

    yield app

@pytest.fixture
def app_client(loop, aiohttp_client, test_app):
    yield loop.run_until_complete(aiohttp_client(test_app))
