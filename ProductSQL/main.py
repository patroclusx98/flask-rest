import schemas

from dataclasses import dataclass
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from constants import (
    DB_URL,
    DB_SECRET_KEY,
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    DEFAULT_SORT_BY,
    DEFAULT_SORT_ORDER,
    SCC_200_OK,
    SCC_201_CREATED,
    ERR_404_NOT_FOUND,
    ERR_409_EXISTS,
    ERR_500_INTERNAL
)
from utils import validate_request, get_order_by, create_response, create_error_response

"""
    TODO
    Write unit tests
"""

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config['SECRET_KEY'] = DB_SECRET_KEY
db = SQLAlchemy(app)


@dataclass
class ProductModel(db.Model):
    barcode: str
    name: str
    count: int

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    count = db.Column(db.Integer, nullable=False)


class ProductAPI(Resource):
    def get(self):
        schema = schemas.ProductGetQuerySchema()
        args = request.args

        validate_request(schema, args)

        try:
            filters = set()
            if ('barcode' in args):
                filters.add(ProductModel.barcode.like(f"%{args['barcode']}%"))
            if ('name' in args):
                filters.add(ProductModel.name.like(f"%{args['name']}%"))

            per_page = args.get('limit', DEFAULT_LIMIT, type=int)
            page = args.get('offset', DEFAULT_OFFSET, type=int)
            sort_by = args.get('sortBy', DEFAULT_SORT_BY, type=str)
            sort_order = args.get('sortOrder', DEFAULT_SORT_ORDER, type=str)

            response = ProductModel.query.filter(
                *filters
            ).order_by(
                get_order_by(ProductModel, sort_by, sort_order)
            ).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            if (response.items):
                return create_response(**SCC_200_OK, data=response.items, meta_data=(response, sort_by, sort_order))
            else:
                return create_error_response(**ERR_404_NOT_FOUND)
        except BaseException as err:
            return create_error_response(**ERR_500_INTERNAL, error_data=err)

    def put(self):
        schema = schemas.ProductPutQuerySchema()
        args = request.form

        validate_request(schema, args)

        try:
            response = ProductModel.query.filter_by(barcode=args["barcode"]).first()
            if (response):
                return create_error_response(**ERR_409_EXISTS)

            new_product = ProductModel(barcode=args["barcode"], name=args["name"], count=args["count"])
            db.session.add(new_product)
            db.session.commit()

            return create_response(**SCC_201_CREATED, data=new_product)
        except BaseException as err:
            return create_error_response(**ERR_500_INTERNAL, error_data=err)

    def patch(self):
        schema = schemas.ProductPatchQuerySchema()
        args = request.form

        validate_request(schema, args)

        try:
            response = ProductModel.query.filter_by(barcode=args["barcode"]).first()

            if (response):
                if ("name" in args and args['name']):
                    response.name = args["name"]
                if ("count" in args and args['count']):
                    response.count = args["count"]

                db.session.commit()

                return create_response(**SCC_200_OK, data=response)
            else:
                return create_error_response(**ERR_404_NOT_FOUND)
        except BaseException as err:
            return create_error_response(**ERR_500_INTERNAL, error_data=err)

    def delete(self):
        schema = schemas.ProductDeleteQuerySchema()
        args = request.form

        validate_request(schema, args)

        try:
            response = ProductModel.query.filter_by(barcode=args["barcode"]).first()
            if (response):
                db.session.delete(response)
                db.session.commit()

                return create_response(**SCC_200_OK, data=response)
            else:
                return create_error_response(**ERR_404_NOT_FOUND)
        except BaseException as err:
            return create_error_response(**ERR_500_INTERNAL, error_data=err)


api.add_resource(ProductAPI, "/product", endpoint="product")

if __name__ == "__main__":
    app.run(debug=True)
