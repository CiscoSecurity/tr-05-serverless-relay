from http import HTTPStatus

from pytest import fixture

from .utils import headers


def routes():
    yield '/respond/observables'
    yield '/respond/trigger'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json(route):
    if route.endswith('/observables'):
        return [{'type': 'unknown', 'value': ''}]

    if route.endswith('/trigger'):
        return {'action_id': 'invalid_action_id',
                'observable_type': 'unknown',
                'observable_value': None}


def test_respond_call_with_valid_jwt_but_invalid_json_failure(route,
                                                              client,
                                                              valid_jwt,
                                                              invalid_json):
    response = client.post(route,
                           headers=headers(valid_jwt),
                           json=invalid_json)
    assert response.status_code == HTTPStatus.OK


@fixture(scope='module')
def valid_json(route):
    if route.endswith('/observables'):
        return [{'type': 'domain', 'value': 'cisco.com'}]

    if route.endswith('/trigger'):
        return {'action-id': 'valid-action-id',
                'observable_type': 'domain',
                'observable_value': 'cisco.com'}


def test_respond_call_success(route, client, valid_jwt, valid_json):
    response = client.post(route, headers=headers(valid_jwt), json=valid_json)
    assert response.status_code == HTTPStatus.OK
