import pytest

from flames_app import app as app_module
from flames_app import database as db_module


@pytest.fixture()
def client(tmp_path):
    test_db = tmp_path / 'test_secret_notes.db'
    db_module.DATABASE = str(test_db)
    db_module.init_db()
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
        yield test_client


def test_create_note_rejects_short_password(client):
    response = client.post(
        '/create-note',
        json={
            'message': 'hello there',
            'password': '123',
            'sender_name': 'tester'
        }
    )

    assert response.status_code == 400
    assert 'Password must be at least' in response.get_json()['error']


def test_expired_note_is_not_viewable(client):
    note_id = db_module.create_note('expired message', 'longpassword', 'tester', expire_days=-1)

    response = client.get(f'/note/{note_id}')

    assert response.status_code == 404


def test_expired_note_cannot_be_unlocked(client):
    note_id = db_module.create_note('expired message', 'longpassword', 'tester', expire_days=-1)

    response = client.post('/unlock-note', json={'note_id': note_id, 'password': 'longpassword'})

    assert response.status_code == 401
    assert response.get_json()['success'] is False


def test_create_note_returns_relative_path(client):
    response = client.post(
        '/create-note',
        json={
            'message': 'safe message',
            'password': 'secure123',
            'sender_name': 'tester'
        }
    )

    body = response.get_json()

    assert response.status_code == 200
    assert body['note_path'].startswith('/note/')