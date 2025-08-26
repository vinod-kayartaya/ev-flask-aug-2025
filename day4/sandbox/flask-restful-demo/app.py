from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
api = Api(app)


# Initialize Limiter
limiter = Limiter(
    get_remote_address,  # Default: limit by client IP
    app=app,
    default_limits=["100 per hour"]  # Global default
)

# initialization of SQLAlchemy db object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employeesdb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Ub7q+c+1itSq4uycrC1ys4CVnPMmr5lkQ2n4pDJy2pmoQ1+4Ldkv9q7VnsMlVPEr'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 365 * 24 * 60 * 60

JWTManager(app) # initialize the JWT manager

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    salary = db.Column(db.Double, nullable=False)
    department = db.Column(db.String)
    job_title = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "salary": self.salary,
            "department": self.department,
            "job_title": self.job_title
        }

    def __repr__(self):
        return f'<Employee (id={self.id!r}, name={self.name!r})>'


def error_response(e, status=400):
    return {"message": e, "when": str(datetime.now())}, status


@app.post("/api/auth/login")
def handle_login():
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')

    if (not username) or (not password):
        return error_response('username/password required', 400)
    
    # hardcoded for simplicity; use DB accessed credentials
    if username != 'admin' or password != 'Welcome#123':
        return error_response('invalid credentials', 401)
    
    token = create_access_token("admin", additional_claims={"role": "ADMIN", "email": "admin@xmpl.com", "fullname": "Administrator"})

    return {"token": token}

class EmployeeResource(Resource):
    @limiter.limit("5 per minute")
    def get(self, emp_id):
        
        emp = Employee.query.get(emp_id)
        if emp:
            return emp.to_dict()
        
        return error_response(f'no data found for id {emp_id}', 404)
    
    @jwt_required()
    def put(self, emp_id):
        emp = Employee.query.get(emp_id)
        if not emp:
            return error_response(f'no data found for id {emp_id}', 404)
        
        payload = request.get_json()
        emp.name = payload.get('name')
        emp.salary = payload.get('salary')
        emp.department = payload.get('department')
        emp.job_title = payload.get('job_title')

        db.session.commit() # changes to emp will be automatically updated
        return emp.to_dict()

    @jwt_required()
    def delete(self, emp_id):
        emp = Employee.query.get(emp_id)
        if emp:
            db.session.delete(emp)
            db.session.commit()
            return None, 204
        
        return error_response(f'no data found for id {emp_id}', 404)

    @jwt_required()
    def patch(self, emp_id):
        emp = Employee.query.get(emp_id)
        if not emp:
            return error_response(f'no data found for id {emp_id}', 404)
        
        payload = request.get_json()
        
        new_name = payload.get('name')
        if new_name: emp.name = new_name

        new_salary = payload.get('salary')
        if new_salary: emp.salary = new_salary

        new_department = payload.get('department')
        if new_department: emp.department = new_department
        
        new_job_title = payload.get('job_title')
        if new_job_title: emp.job_title = new_job_title

        db.session.commit() # changes to emp will be automatically updated
        return emp.to_dict()

class EmployeeListResource(Resource):
    
    @limiter.limit("5 per minute")
    def get(self):
        return [e.to_dict() for e in Employee.query.all()]

    @jwt_required()
    def post(self):
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
        
        emp = Employee()
        emp.name = new_employee.get('name')
        emp.department = new_employee.get('department')
        emp.salary = new_employee.get('salary')
        emp.job_title = new_employee.get('job_title')

        db.session.add(emp)
        db.session.commit()

        return emp.to_dict(), 201

api.add_resource(EmployeeListResource, "/api/employees")
api.add_resource(EmployeeResource, "/api/employees/<int:emp_id>")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8080, debug=True)