from datetime import datetime

from authlib.jose import jwt
from pytest import fixture

from app import app


@fixture(scope='session')
def secret_key():
    # Generate some string based on the current date & time.
    return datetime.utcnow().isoformat()


@fixture(scope='session')
def client(secret_key):
    app.secret_key = secret_key

    app.testing = True

    with app.test_client() as client:
        yield client


@fixture(scope='session')
def valid_jwt(secret_key):
    header = {'alg': 'HS256'}

    payload = {'username': 'gdavoian'}

    return jwt.encode(header, payload, secret_key).decode('ascii')


@fixture(scope='session')
def invalid_jwt(valid_jwt):
    # Corrupt the JWT by reversing its signature.
    header, payload, signature = valid_jwt.split('.')
    return header + '.' + payload + '.' + signature[::-1]
