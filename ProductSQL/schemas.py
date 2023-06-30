import main

from marshmallow import Schema, fields
from marshmallow.validate import Range, OneOf

from constants import SORT_ORDER_VALUES


class ProductGetQuerySchema(Schema):
    barcode = fields.Str(required=False)
    name = fields.Str(required=False)
    limit = fields.Int(required=False, validate=Range(min=1, error="Value must be greater than 0"))
    offset = fields.Int(required=False, validate=Range(min=0, error="Value must be equal or greater than 0"))
    sortBy = fields.Str(required=False, validate=OneOf(
        choices=list(main.ProductModel.__dataclass_fields__.keys()),
        error="The specified value is not a valid column header"
    ))
    sortOrder = fields.Str(required=False, validate=OneOf(
        choices=SORT_ORDER_VALUES, error=f"Value must be one of the following: {SORT_ORDER_VALUES}"
    ))


class ProductPutQuerySchema(Schema):
    barcode = fields.Str(required=True)
    name = fields.Str(required=True)
    count = fields.Int(required=True)


class ProductPatchQuerySchema(Schema):
    barcode = fields.Str(required=True)
    name = fields.Str(required=False)
    count = fields.Int(required=False)


class ProductDeleteQuerySchema(Schema):
    barcode = fields.Str(required=True)
