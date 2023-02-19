from flask import jsonify, make_response, abort
from flask_sqlalchemy import model, pagination
from marshmallow import Schema

from constants import ERR_400_CLIENT


def validate_request(schema: Schema, request_fields):
    # Validates the given request by the specified schema; Throws 400 exception if there are any errors

    errors = schema.validate(request_fields)
    if (errors):
        abort(ERR_400_CLIENT['status_code'], {"message": ERR_400_CLIENT['message'], "errorInfo": str(errors)})


def get_order_by(model: model.Model, sort_by: str, sort_order: str):
    # Returns ascending or descending sort query based on given arguments

    return (getattr(model, sort_by) if sort_order == "ASC" else getattr(model, sort_by).desc())


def make_metadata(meta_data: tuple[pagination.QueryPagination, str, str]):
    # Creates a dictionary of pagination and sorting metadata details for GET requests

    pagination_data, sort_by, sort_order = meta_data
    return {
        "limit": pagination_data.per_page,
        "offset": pagination_data.page,
        "totalItems": pagination_data.total,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }


def create_response(status_code: int, message: str, data=None, meta_data: tuple[pagination.QueryPagination, str, str] = None):
    # Creates a Response object based on given arguments to be used for 1xx, 2xx and 3xx responses

    data_set = dict()
    if (data):
        data_set.update({"data": data})
    if (meta_data):
        data_set.update({"metadata": make_metadata(meta_data)})

    return make_response(jsonify(message=message, **data_set), status_code)


def create_error_response(status_code: int, message: str, error_data=None):
    # Creates a Response object based on given arguments to be used for 4xx and 5xx responses

    if (not error_data):
        return make_response(jsonify(message=message), status_code)
    else:
        return make_response(jsonify(message=message, errorInfo=str(error_data)), status_code)
