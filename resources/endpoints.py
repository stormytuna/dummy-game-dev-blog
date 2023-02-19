from flask_restful import Resource
import json


class Endpoints(Resource):
    def get(self):
        with open("./db/data/endpoints.json") as endpoints_file:
            endpoints_data = endpoints_file.read()
            endpoints = json.loads(endpoints_data)
            return endpoints
