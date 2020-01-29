from flask import jsonify


def json_ok(data):
    return jsonify({'data': data})
