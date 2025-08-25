"""
In flask-restful, these are important concepts:

- Resource -> class representing an endpoint
- api -> wrapper around the flask app
- methods -> GET/POST/PUT/PATCH/DELETE represented as methods in a resource


- one resource for GET/PUT/PATCH/DELETE (operations based on resource id)
    ex: /api/employees/<int:id>
- one resource for GET/POST (operations on a collection)
    ex: /api/employees

"""

from flask import Flask, request
from flask_restful import Resource, Api
import json
from datetime import datetime

app = Flask(__name__)
api = Api(app)

_employees = []

# load data from employees.json
with open('employees.json', encoding='utf-8') as f:
    _employees = json.load(f)

next_id = max([e['id'] for e in _employees]) + 1

def error_response(e, status=400):
    return {"message": e, "when": str(datetime.now())}, status


class EmployeeResource(Resource):
    def get(self, emp_id):
        result = [e for e in _employees if e['id']==emp_id]
        if len(result):
            return result[0], 200
        return error_response(f'no data found for id {emp_id}', 404)
    
    def put(self, emp_id):
        return "update not implemented yet", 400

    def delete(self, emp_id):
        return "delete not implemented yet", 400

    def patch(self, emp_id):
        return "partial update not implemented yet", 400

class EmployeeListResource(Resource):
    def get(self):
        return _employees, 200

    def post(self):
        global next_id

        req_body = request.get_json()
        # validation for missing fields
        required_fields = ['name', 'salary']
        missing_fields = []

        for f in required_fields:
            if not f in req_body:
                missing_fields.append(f)

        if len(missing_fields)>0:
            return error_response(f'missing fields: {missing_fields}')
       
        all_fields = ['name', 'department', 'salary', 'job_title']
        new_employee = {k:req_body.get(k) for k in all_fields}
        new_employee['id'] = next_id
        
        next_id += 1

        _employees.append(new_employee)
        
        with open('./employees.json', 'wt') as file:
            json.dump(_employees, file)

        return new_employee, 201

api.add_resource(EmployeeListResource, "/api/employees")
api.add_resource(EmployeeResource, "/api/employees/<int:emp_id>")

app.run(host="0.0.0.0", port=8080, debug=True)