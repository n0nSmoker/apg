import pathlib
import ssl

from aiohttp import web
from aiohttp.test_utils import unused_port


class BaseFakeAPI:
    def __init__(self, *, loop, host):
        self.loop = loop
        self.host = host
        self.app = web.Application(loop=loop)
        self.add_routes()
        self.runner = None
        here = pathlib.Path(__file__)
        ssl_cert = here.parent / 'server.crt'
        ssl_key = here.parent / 'server.key'
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(str(ssl_cert), str(ssl_key))

    def add_routes(self):
        pass

    async def start(self):
        port = unused_port()
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, '127.0.0.1', port, ssl_context=self.ssl_context)
        await site.start()
        return {self.host: port}

    async def stop(self):
        await self.runner.cleanup()
