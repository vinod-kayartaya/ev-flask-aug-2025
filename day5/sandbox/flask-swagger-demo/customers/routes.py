from flask import Blueprint, request, jsonify
from extensions import db
from models import Customer
from flasgger.utils import swag_from

customers_bp = Blueprint("customers", __name__, url_prefix="/api/customers")


@customers_bp.route("/", methods=["POST"])
@swag_from({
    "tags": ["Customers"],
    "description": "Create a new customer",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "city": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                },
                "required": ["name", "email", "phone"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Customer created successfully",
            "examples": {
                "application/json": {
                    "id": 1,
                    "name": "Vinod",
                    "city": "Bangalore",
                    "email": "vinod@vinod.co",
                    "phone": "9731424784"
                }
            }
        },
        400: {"description": "Validation error"},
        409: {"description": "Email already exists"}
    }
})
def create_customer():
    """Endpoint to create a customer"""
    data = request.json
    name, city, email, phone = data.get("name"), data.get("city"), data.get("email"), data.get("phone")

    if not (name and email and phone):
        return jsonify({"error": "name, email, phone are required"}), 400

    if Customer.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 409

    customer = Customer(name=name, city=city, email=email, phone=phone)
    db.session.add(customer)
    db.session.commit()

    return jsonify(customer.to_dict()), 201


@customers_bp.route("/", methods=["GET"])
@swag_from({
    "tags": ["Customers"],
    "description": "List all customers",
    "responses": {
        200: {
            "description": "A list of customers",
            "examples": {
                "application/json": [
                    {
                        "id": 1,
                        "name": "Vinod",
                        "city": "Bangalore",
                        "email": "vinod@vinod.co",
                        "phone": "9731424784"
                    }
                ]
            }
        }
    }
})
def list_customers():
    """Endpoint to list customers"""
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])