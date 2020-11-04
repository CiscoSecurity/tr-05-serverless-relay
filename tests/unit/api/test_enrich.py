from http import HTTPStatus

from pytest import fixture

from api.schemas import OBSERVABLE_TYPE_CHOICES
from .utils import headers


def routes():
    yield '/deliberate/observables'
    yield '/observe/observables'
    yield '/refer/observables'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json_value():
    return [{'type': 'ip', 'value': ''}]


@fixture(scope='module')
def invalid_json_type():
    return [{'type': 'strange', 'value': 'cisco.com'}]


def test_enrich_call_with_valid_jwt_but_invalid_json_value(
        route, client, valid_jwt, invalid_json_value,
        invalid_json_expected_payload
):
    response = client.post(route,
                           headers=headers(valid_jwt),
                           json=invalid_json_value)
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_json_expected_payload(
        "{0: {'value': ['Field may not be blank.']}}"
    )


def test_enrich_call_with_valid_jwt_but_invalid_json_type(
        route, client, valid_jwt, invalid_json_type,
        invalid_json_expected_payload
):
    allowed_fields = ", ".join(map(repr, OBSERVABLE_TYPE_CHOICES))
    response = client.post(route,
                           headers=headers(valid_jwt),
                           json=invalid_json_type)
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_json_expected_payload(
        '{0: {\'type\': ["Must be one of: ' + allowed_fields + '."]}}'
    )


@fixture(scope='module')
def valid_json():
    return [{'type': 'domain', 'value': 'cisco.com'}]


def test_enrich_call_success(route, client, valid_jwt, valid_json):
    response = client.post(route, headers=headers(valid_jwt), json=valid_json)
    assert response.status_code == HTTPStatus.OK
