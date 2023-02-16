from flask import Flask
from flask_restful import Api, Resource

# Initialise the Flask app and wrap it in an RESTful API
app = Flask(__name__)
api = Api(app)


class HelloWorldAPI(Resource):
    # Defines the Hello World resource

    def get(self):
        # Defines the GET request method

        return {"message": "Hello World"}, 200


# Adds the Hello World resource to the defined URI
api.add_resource(HelloWorldAPI, "/helloworld", endpoint="helloworld")

# Run the Flask server in debug mode
if __name__ == "__main__":
    app.run(host="localhost", debug=True)
