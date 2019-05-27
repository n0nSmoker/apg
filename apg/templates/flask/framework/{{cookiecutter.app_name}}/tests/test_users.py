from app.users.models import User


module_name = 'user'

USER_DATA = {
    'name': 'new_test_user',
    'password': 'testPassword',
}

TEST_404_PARAMS = {
    'user_id': 42,
    'check_status': 404
}


def test_current_user(client, test_user):
    resp = client.get(
        endpoint=f'{module_name}s.current_{module_name}_view',
        headers={'X-Auth-Token': test_user.access_token}
    )
    assert 'data' in resp
    data = resp['data']
    assert test_user.to_dict() == data


def test_create_user(client, test_user):
    resp = client.post(
        endpoint=f'{module_name}s.add_{module_name}_view',
        data={
            **USER_DATA
        },
        headers={'X-Auth-Token': test_user.access_token}
    )
    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    assert User.query.filter_by(id=data['id']).one_or_none()
    assert USER_DATA['name'] == data['name']


def test_user_list(client, test_user):
    resp = client.get(
        endpoint=f'{module_name}s.list_view',
        headers={'X-Auth-Token': test_user.access_token}
    )
    assert 'data' in resp
    data = resp['data']
    assert 'results' in data
    assert 'total' in data
    for user in data['results']:
        assert 'id' in user
        assert 'name' in user
        assert 'password' not in user


def test_user_by_id(client, test_user):
    request_params = {
        'endpoint': f'{module_name}s.{module_name}_by_id_view',
        'headers': {'X-Auth-Token': test_user.access_token}
    }
    resp = client.get(
        **request_params,
        user_id=User.query.first().id,
    )
    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    assert 'name' in data
    assert 'password' not in data

    client.get(
        **request_params,
        **TEST_404_PARAMS
    )


def test_update_user(client, test_user):
    new_name = 'updated_test_name'
    new_password = 'updated_test_password'
    request_params = {
        'endpoint': f'{module_name}s.update_{module_name}_view',
        'name': new_name,
        'password': new_password,
        'headers': {'X-Auth-Token': test_user.access_token}
    }
    resp = client.put(
        **request_params,
        user_id=User.query.first().id,
    )
    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    assert data['name'] == new_name
    assert User.query.filter_by(id=data['id']).one().to_dict() == data

    client.put(
        **request_params,
        **TEST_404_PARAMS
    )


def test_delete_user(client, test_user):
    request_params = {
        'endpoint': f'{module_name}s.delete_{module_name}_view',
        'headers': {'X-Auth-Token': test_user.access_token}
    }
    resp = client.delete(
        **request_params,
        user_id=User.query.first().id,
    )
    assert 'data' in resp
    data = resp['data']
    assert not User.query.filter_by(id=data['id']).one_or_none()

    client.delete(
        **request_params,
        **TEST_404_PARAMS
    )
