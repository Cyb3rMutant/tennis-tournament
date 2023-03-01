import pytest
from app import app as a


@pytest.fixture()
def app():
    app = a
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_login_fail_user(client):
    response = client.post(
        '/login/', data={'email': 'user@gmail.com', 'password': ''})
    # response = client.get('/login/')
    assert b"user not found" in response.data


def test_login_fail_pass(client):
    response = client.post(
        '/login/', data={'email': 'test@t.c', 'password': 'hhhhhh'})
    # response = client.get('/login/')
    assert b"incorrect password" in response.data


def test_login_success(client):
    response = client.post(
        '/login/', data={'email': 'test@t.c', 'password': ''})
    # response = client.get('/login/')
    assert b"success" in response.data
