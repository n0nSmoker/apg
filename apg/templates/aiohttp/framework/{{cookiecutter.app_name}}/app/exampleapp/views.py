from app.exampleapp.schemas import EXAMPLE_JSON_SCHEMA, EXAMPLE_SCHEMA, EXAMPLE_UPDATE_SCHEMA
from lib.api import ExampleAPI
from lib.utils import RouteTableDef, success
from lib.webforms import use_kwargs


routes = RouteTableDef(url_prefix='/example')


@routes.get('/')
@use_kwargs(EXAMPLE_SCHEMA)
async def example_view(request, int_field, str_field):
    api = ExampleAPI(session=request.app['client_session'])

    result = await api.example(
        int_field=int_field,
        str_field=str_field,
    )
    return success(result)


@routes.post('/')
@use_kwargs({**EXAMPLE_JSON_SCHEMA}, locations=['json'])
async def example_json_view(request, **kwargs):
    api = ExampleAPI(session=request.app['client_session'])

    result = await api.example_json(
        kwargs=kwargs
    )
    return success(result)


@routes.put(r'/{item_id:\d+}/')
@use_kwargs(EXAMPLE_UPDATE_SCHEMA)
async def example_update_view(request, int_field, str_field):
    item_id = request.match_info['item_id']
    api = ExampleAPI(session=request.app['client_session'])

    result = await api.example_update(
        int_field=int_field,
        str_field=str_field,
        item_id=item_id
    )
    return success(result)


@routes.delete(r'/{item_id:\d+}/')
async def example_delete_view(request):
    item_id = request.match_info['item_id']
    api = ExampleAPI(session=request.app['client_session'])

    result = await api.example_delete(
        item_id=item_id
    )
    return success(result)
