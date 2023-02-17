from flask import Flask, request, abort
from flask_restful import Api, Resource
from marshmallow import Schema, fields


app = Flask(__name__)
api = Api(app)

# Dictionary to store product data
products = {}


class ProductGetQuerySchema(Schema):
    # Schema for GET request validation

    barcode = fields.Str(required=False)


class ProductPutQuerySchema(Schema):
    # Schema for PUT/PATCH request validation

    barcode = fields.Str(required=True)
    name = fields.Str(required=True)
    count = fields.Int(required=True)


class ProductDeleteQuerySchema(Schema):
    # Schema for DELETE request validation

    barcode = fields.Str(required=True)


class ProductAPI(Resource):
    # Defines the Product CRUD resource

    def get(self):
        schema = ProductGetQuerySchema()
        args = request.args

        # Validates the request against the GET schema
        errors = schema.validate(args)
        if (errors):
            abort(400, str(errors))

        # If barcode given, filter and display products
        barcode = args.get("barcode", None)
        if (barcode and barcode in products):
            return {"message": "Success", "data": products[barcode]}, 200
        elif (barcode):
            return {"message": "Product(s) not found"}, 404

        # If no barcode given, display all products in dictionary
        if (len(products) > 0):
            return {"message": "Success", "data": products}, 200
        else:
            return {"message": "Product(s) not found"}, 404

    def put(self):
        schema = ProductPutQuerySchema()
        args = request.form

        # Validates the request against the PUT/PATCH schema
        errors = schema.validate(args)
        if (errors):
            abort(400, str(errors))

        # Checks if product already exists
        barcode = args.get("barcode", None)
        if (barcode and barcode in products):
            return {"message": "Product already exists"}, 409

        # Adds product into dictionary
        products[barcode] = args
        return {"message": "Success", "data": products[barcode]}, 201

    def patch(self):
        schema = ProductPutQuerySchema()
        args = request.form

        # Validates the request against the PUT/PATCH schema
        errors = schema.validate(args)
        if (errors):
            abort(400, str(errors))

        # Updates the specified product's details in the dictionary
        barcode = args.get("barcode", None)
        if (barcode and barcode in products):
            products[barcode] = args
            return {"message": "Success", "data": products[barcode]}, 200
        elif (barcode):
            return {"message": "Product not found"}, 404

    def delete(self):
        schema = ProductDeleteQuerySchema()
        args = request.form

        # Validates the request against the DELETE schema
        errors = schema.validate(args)
        if (errors):
            abort(400, str(errors))

        # Deletes the specified product from the dictionary
        barcode = args.get("barcode", None)
        if (barcode and barcode in products):
            product_to_delete = products.pop(barcode)
            return {"message": "Success", "data": product_to_delete}, 200

        return {"message": "Product not found"}, 404


api.add_resource(ProductAPI, "/product", endpoint="product")

if __name__ == "__main__":
    app.run(debug=True)
