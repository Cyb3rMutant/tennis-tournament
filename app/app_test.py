import pytest
from app import app as a
import certifi
from pymongo import MongoClient
ca = certifi.where()
cluster = "mongodb+srv://strings:6Zd69XPFvPbt0Wfw@tennis-tournament.v5i5qjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=ca)
db = client.TennisDB


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


def test_001_login_fail_user_does_not_exist(client):
    response = client.post(
        '/login/', data={'email': 'jgiohres@jfl.da', 'password': 'something'})
    # response = client.get('/login/')
    assert b"user not found" in response.data


def test_002_login_fail_wrong_password(client):
    response = client.post(
        '/login/', data={'email': 'test@t.c', 'password': 'hhhhhh'})
    # response = client.get('/login/')
    assert b"incorrect password" in response.data


def test_003_login_success(client):
    response = client.post(
        '/login/', data={'email': 'test@t.c', 'password': ''})
    # response = client.get('/login/')
    assert b"success" in response.data


def test_004_add_admin_fial_user_exists(client):
    response = client.post(
        '/add-admin/', data={'name': 'someooooooooooo', 'email': 'test@t.c', 'password': 'someone', 'confirm': 'someone', 'accept_tos': True})
    # response = client.get('/login/')
    assert b"user already exists" in response.data


def test_005_add_admin_success(client):
    response = client.post(
        '/add-admin/', data={'name': 'someooooooooooo', 'email': 'helllllllllooooofdsa@t.c', 'password': 'someone', 'confirm': 'someone', 'accept_tos': True})
    # response = client.get('/login/')
    db.admins.delete_one(
        {'name': 'someooooooooooo', 'email': 'helllllllllooooofdsa@t.c'})
    assert b"success" in response.data
