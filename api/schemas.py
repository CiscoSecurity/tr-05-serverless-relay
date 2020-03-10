from functools import partial

from marshmallow import ValidationError, Schema, fields, INCLUDE


def validate_string(value, *, choices=None):
    if value == '':
        raise ValidationError('Field may not be blank.')

    if choices is not None:
        if value not in choices:
            raise ValidationError(
                f'Must be one of: {", ".join(map(repr, choices))}.'
            )


OBSERVABLE_TYPE_CHOICES = (
    'amp_computer_guid',
    'certificate_common_name',
    'certificate_issuer',
    'certificate_serial',
    'cisco_mid',
    'device',
    'domain',
    'email',
    'email_messageid',
    'email_subject',
    'file_name',
    'file_path',
    'hostname',
    'imei',
    'imsi',
    'ip',
    'ipv6',
    'mac_address',
    'md5',
    'mutex',
    'ngfw_id',
    'ngfw_name',
    'odns_identity',
    'odns_identity_label',
    'orbital_node_id',
    'pki_serial',
    'process_name',
    'registry_key',
    'registry_name',
    'registry_path',
    'sha1',
    'sha256',
    'url',
    'user',
    'user_agent',
)


class ObservableSchema(Schema):
    type = fields.String(
        validate=partial(validate_string, choices=OBSERVABLE_TYPE_CHOICES),
        required=True,
    )
    value = fields.String(
        validate=validate_string,
        required=True,
    )


class ActionFormParamsSchema(Schema):
    action_id = fields.String(
        data_key='action-id',
        validate=validate_string,
        required=True,
    )
    observable_type = fields.String(
        validate=partial(validate_string, choices=OBSERVABLE_TYPE_CHOICES),
        required=True,
    )
    observable_value = fields.String(
        validate=validate_string,
        required=True,
    )

    class Meta:
        unknown = INCLUDE
