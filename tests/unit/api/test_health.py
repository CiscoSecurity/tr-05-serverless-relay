from http import HTTPStatus

from pytest import fixture

from .utils import headers


def routes():
    yield '/health'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


def test_health_call_without_jwt_failure(route, client):
    response = client.post(route)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_health_call_with_invalid_jwt_failure(route, client, invalid_jwt):
    response = client.post(route, headers=headers(invalid_jwt))
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_health_call_success(route, client, valid_jwt):
    response = client.post(route, headers=headers(valid_jwt))
    assert response.status_code == HTTPStatus.OK
