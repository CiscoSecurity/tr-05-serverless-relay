from flask import request, jsonify
from werkzeug.exceptions import BadRequest


def get_json(schema):
    """
    Parse the incoming request data as JSON and validate it against a schema.

    Note. This function is just an example of how one can read and check the
    input data before passing to an API endpoint, and thus it may be modified
    in any way, replaced by another function, or even removed from the module.
    """

    data = request.get_json(force=True, silent=True, cache=False)

    message = schema.validate(data)

    if message:
        raise BadRequest(message)

    return data


def jsonify_data(data):
    return jsonify({'data': data})
