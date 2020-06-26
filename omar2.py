from flask import Flask, request,make_response
from flask_restful  import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import jsonify

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)


class Employees(Resource):
    def get(self):
        return make_response({'get':'ss'})  # Fetches first column that is Employee ID

    def post(self):
        return  make_response({'m':'nothing'})
class Employees_Name(Resource):
    def post(self,id):
        print(request.get_json())
        print(id)
        return {'employees':"post"}


api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Employees_Name, '/employees2/<int:id>',endpoint='id')  # Route_3

if __name__ == '__main__':
    app.run(port='5002')