from flask import Blueprint, request, jsonify
from extensions import db
from models import Customer

customers_bp = Blueprint("customers", __name__, url_prefix="/api/customers")

@customers_bp.route("/", methods=["POST"])
def create_customer():
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
def list_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])

@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict())