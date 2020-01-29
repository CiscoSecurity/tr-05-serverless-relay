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
    'pki_serial',
    'sha1',
    'sha256',
    'url',
    'user',
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
