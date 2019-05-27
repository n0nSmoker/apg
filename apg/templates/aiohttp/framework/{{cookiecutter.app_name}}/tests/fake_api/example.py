from aiohttp import web
from yarl import URL

from config import EXAMPLE_API_DOMAIN

from .base import BaseFakeAPI


API_URL_PREFIX = URL(EXAMPLE_API_DOMAIN).path


# TODO: use it for mocking PushAPI behavior #noqa
class FakeExampleAPI(BaseFakeAPI):
    def add_routes(self):
        self.app.router.add_routes([
            web.post(f'{API_URL_PREFIX}/test/route', self.test_route),
        ])

    async def test_route(self, request):
        response = request
        return web.json_response(response)
