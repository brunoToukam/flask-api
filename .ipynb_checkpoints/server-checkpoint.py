from curses import resetty
from distutils.log import debug
from flask import Flask
from flask_restful import Api, Resource

# app
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello World!"}

api.add_resource(HelloWorld, '/hi')


if __name__ == "__main__":
    app.run(debug=True)

