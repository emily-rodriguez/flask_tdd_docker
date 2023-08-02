import json

from src.api.models import User


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    username = 'barbie'
    email = 'barbie@barbieland.com'
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': username,
            'email': email
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert f'{email} was added!' in data['message']


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({"email": "ken@mojodojocasahouse.com"}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/users',
        data=json.dumps({
            'username': 'skipper',
            'email': 'skipper@barbieland.com'
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'skipper',
            'email': 'skipper@barbieland.com'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That email already exists.' in data['message']


def test_single_user(test_app, test_database, add_user):
    user = add_user(username='midge', email='midge@barbieland.com')
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'midge' in data['username']
    assert 'midge@barbieland.com' in data['email']


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/users/999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User 999 does not exist' in data['message']

def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user('allan', 'allan@barbieland.com')
    add_user('barbie', 'barbie@barbieland.com')
    client = test_app.test_client()
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'allan' in data[0]['username']
    assert 'allan@barbieland.com' in data[0]['email']
    assert 'barbie' in data[1]['username']
    assert 'barbie@barbieland.com' in data[1]['email']
