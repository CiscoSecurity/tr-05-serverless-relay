from http import HTTPStatus

from pytest import fixture

from api.schemas import PERIODS_CHOICES
from api.errors import INVALID_ARGUMENT
from .utils import get_headers


allowed_periods = ", ".join(map(repr, PERIODS_CHOICES))


def routes():
    yield '/dashboard/tiles'
    yield '/dashboard/tiles/module_instants_id/tile_id'
    yield '/dashboard/tiles/module_instants_id/tile_id/data'


@fixture(scope='module', params=routes(), ids=lambda route: f'GET {route}')
def route(request):
    return request.param


@fixture()
def invalid_params_data():
    return {'period': 'invalid_data'}


@fixture()
def invalid_params_name():
    return {'invalid_name': 'last_7_days'}


@fixture(scope='module')
def invalid_params_expected_payload():
    def _make_message(message):
        return {
            'errors': [{
                'code': INVALID_ARGUMENT,
                'message': message,
                'type': 'fatal'
            }]
        }

    return _make_message


def test_dashboard_call_with_invalid_params_data(
        client, valid_jwt, invalid_params_data,
        invalid_params_expected_payload,
        route='/dashboard/tiles/module_instants_id/tile_id/data'

):
    response = client.get(route, headers=get_headers(valid_jwt),
                          query_string=invalid_params_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_params_expected_payload(
        '{\'period\': '
        '["Must be one of: ' + allowed_periods + '."]}'
    )


def test_dashboard_call_with_invalid_params_name(
        client, valid_jwt, invalid_params_name,
        invalid_params_expected_payload,
        route='/dashboard/tiles/module_instants_id/tile_id/data'

):
    response = client.get(route, headers=get_headers(valid_jwt),
                          query_string=invalid_params_name)

    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_params_expected_payload(
        "{'invalid_name': ['Unknown field.']}"
    )


def test_dashboard_call_success(route, client, valid_jwt):
    response = client.get(route, headers=get_headers(valid_jwt))
    assert response.status_code == HTTPStatus.OK
