from aiohttp import web

from lib.utils import RouteTableDef


routes = RouteTableDef()


@routes.get('/')
async def root_view(request):  # noqa
    return web.Response(text='Hello World')
