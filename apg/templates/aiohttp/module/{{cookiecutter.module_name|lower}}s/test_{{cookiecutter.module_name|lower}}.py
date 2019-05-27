import pytest

from app.{{cookiecutter.module_name|lower}}s.models import {{cookiecutter.module_name|capitalize}}


@pytest.fixture
async def test_{{cookiecutter.module_name|lower}}(app_client):
    return await {{cookiecutter.module_name|capitalize}}.create()


async def test_add_{{cookiecutter.module_name|lower}}_view(app_client):
    resp = await app_client.post('/{{cookiecutter.module_name|lower}}s/')
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    data = resp_json['data']
    assert 'id' in data
    test = await {{cookiecutter.module_name|capitalize}}.query.where({{cookiecutter.module_name|capitalize}}.id == int(data['id'])).gino.first()
    assert data == test.to_dict()


async def test_{{cookiecutter.module_name|lower}}_by_id_view(app_client, test_{{cookiecutter.module_name|lower}}):
    {{cookiecutter.module_name|lower}} = await {{cookiecutter.module_name|capitalize}}.get(test_{{cookiecutter.module_name|lower}}.id)
    resp = await app_client.get(f'/{{cookiecutter.module_name|lower}}s/{% raw %}{{% endraw %}{{cookiecutter.module_name|lower}}.id}/')
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    data = resp_json['data']
    assert data['id'] == {{cookiecutter.module_name|lower}}.id


async def test_list_view(app_client, test_{{cookiecutter.module_name|lower}}):  # noqa
    resp = await app_client.get('/{{cookiecutter.module_name|lower}}s/')
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    data = resp_json['data']
    assert 'results' in data
    assert int(data['total']) == len(data['results'])
    for res in data['results']:
        assert 'id' in res
        assert 'created_at' in res
        assert 'updated_at' in res


async def test_update_{{cookiecutter.module_name|lower}}_view(app_client, test_{{cookiecutter.module_name|lower}}):
    resp = await app_client.put(f'/{{cookiecutter.module_name|lower}}s/{test_{{cookiecutter.module_name|lower}}.id}/')
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    data = resp_json['data']
    test = await {{cookiecutter.module_name|capitalize}}.get(test_{{cookiecutter.module_name|lower}}.id)
    assert data['updated_at'] == test.updated_at.strftime('%Y-%m-%d %H:%M')


async def test_delete_{{cookiecutter.module_name|lower}}_view(app_client, test_{{cookiecutter.module_name|lower}}):
    resp = await app_client.delete(f'/{{cookiecutter.module_name|lower}}s/{test_{{cookiecutter.module_name|lower}}.id}/')
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'data' in resp_json
    data = resp_json['data']
    {{cookiecutter.module_name|lower}} = await {{cookiecutter.module_name|capitalize}}.get(data['id'])
    assert not {{cookiecutter.module_name|lower}}
