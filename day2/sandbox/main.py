"""
/api/customers
GET, POST

/api/customers/<id>
GET, PUT, PATCH, DELETE

/api/customers
/api/customers?page=2
/api/customers?size=20
/api/customers?page=2&size=25

"""

from flask import Flask, jsonify, request
import json
import time
import uuid

# pip install email-validator
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

# load all customer data into memory
_customers = []
with open('./customers.json', encoding='utf-8') as file:
    _customers = json.load(file)

def err_response(message, code=400):
    return jsonify({
        'message': message,
        'timestamp': time.time(),
        'code': code
    }), code


@app.get('/api/v2/customers')
@app.get('/api/customers')
def handle_get_many():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        if page < 1 or size < 1:
            return err_response('page/size must be more than 0')
    except ValueError:
        return err_response('page/size must be integers')
    
    start = (page-1) * size
    end = start + size

    return jsonify(_customers[start:end])

@app.get('/api/v1/customers')
def handle_get_many_v1():
    return jsonify(_customers)


@app.post('/api/customers')
@app.post('/api/v2/customers')
@app.post('/api/v1/customers')
def handle_post():
    req_body = request.get_json()

    # validation for missing fields
    required_fields = ['name', 'email', 'phone']
    missing_fields = []

    for f in required_fields:
        if not f in req_body:
            missing_fields.append(f)

    if len(missing_fields)>0:
        return err_response(f'missing fields: {missing_fields}')
    

    # check if the email is a valid one or not
    email = req_body.get('email')
    try:
        validate_email(email, check_deliverability=True)
        # it's a valid email, just skip!
    except EmailNotValidError as e:
        return err_response(str(e))

    # validation for duplicate email
    all_emails = [c['email'] for c in _customers if 'email' in c]
    if email in all_emails:
        return err_response(f'email already exists - {email}')
    
    # validation for duplicate phone
    all_phones = [c['phone'] for c in _customers if 'phone' in c]
    if req_body.get('phone') in all_phones:
        return err_response(f'phone already exists - {req_body.get('phone')}')

    # copy only these fields from the request body
    all_fields = ['name', 'gender', 'email', 'phone', 'address', 'city', 'country']
    new_customer = {k:req_body.get(k) for k in all_fields}

    # assign an auto-generated id
    new_customer['id'] = str(uuid.uuid4())
    _customers.append(new_customer)
    
    # replace the file content with latest data in the variable _customers
    with open('./customers.json', 'wt') as file:
        json.dump(_customers, file)

    return jsonify(new_customer), 201


@app.get("/api/customers/<uuid:customer_id>")
@app.get("/api/v1/customers/<uuid:customer_id>")
@app.get("/api/v2/customers/<uuid:customer_id>")
def handle_get_one(customer_id):
    customer_id = str(customer_id)
    filtered_customers = [c for c in _customers if c.get('id') == customer_id]

    if len(filtered_customers) == 0:
        return err_response(f'customer with id {customer_id} not found')
    
    return jsonify(filtered_customers[0])


app.run(debug=True, host="0.0.0.0", port=5002)
