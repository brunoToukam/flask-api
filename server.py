from curses import resetty
from distutils.log import debug
from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import train

# app
app = Flask(__name__)
api = Api(app)

recommend_get_args = reqparse.RequestParser()
recommend_get_args.add_argument('name', type=str, help='Name of the investor')
recommend_get_args.add_argument('fundingType', type=str, help='Choose if the type is Pre-Serie A, Serie A,...')
recommend_get_args.add_argument('location', type=str, help='Location of the investor')
recommend_get_args.add_argument('description', type=str, help='Brieve Description of the investor')
recommend_get_args.add_argument('fullDescription', type=str, help='Full description of the investor')

recommends = {}

class Recommend(Resource):
    def get(self, investor_id):
        companies = pd.read_csv('/home/bruno/Downloads/companies.csv')
        return recommends[investor_id]
    

    def put(self, investor_id):
        args = recommend_get_args.parse_args()
        companies = pd.read_csv('/home/bruno/Downloads/companies.csv')
        print('arrrrrrrrgs=', args['name'])
        r = train.recommendations(args['name'], args['fundingType'], args['location'], args['description'], args['fullDescription'], companies)
        print('recommmmmmmmendations = ', r)
        return {args['name']: r}


api.add_resource(Recommend, "/recommend/startups/<int:investor_id>")
#api.add_resource(HelloWorld, '/hi/<name>/<fundingType>/<location>/<description>/<fullDescription>')


if __name__ == "__main__":
    app.run(debug=True)

