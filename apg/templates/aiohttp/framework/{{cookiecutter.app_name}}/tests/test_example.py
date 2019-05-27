async def test_example_view(app_client):
    params = {
        'int_field': 666,
        'str_field': 'Gilfoyle',
    }
    resp = await app_client.get('/example/', params=params)
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    assert resp_json['data']['int_field'] == params['int_field']
    assert resp_json['data']['str_field'] == params['str_field']


async def test_example_update(app_client):
    params = {
        'int_field': 666,
        'str_field': 'Gilfoyle',
    }
    item_id = 1
    resp = await app_client.put(f'/example/{item_id}/', params=params)
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    assert resp_json['data']['int_field'] == params['int_field']
    assert resp_json['data']['str_field'] == params['str_field']


async def test_example_json(app_client):
    json = {
        'test_nesting': [
            {
                'int_param': 34,
                'str_param': 'foo'
            },
            {
                'int_param': 43,
                'str_param': 'bar'
            }
        ]
    }
    resp = await app_client.post('/example/', json=json)
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    assert resp_json['data'] == json
    for item in resp_json['data']['test_nesting']:
        assert item['int_param']
        assert item['str_param']


async def test_example_delete(app_client):
    item_id = 1

    resp = await app_client.delete(f'/example/{item_id}/')

    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    assert resp_json['data']['item_id'] == str(item_id)
    assert resp_json['data']['message'] == 'successfully deleted'
