from flask import Blueprint, jsonify, request

cat_bp = Blueprint("categories", __name__, url_prefix="/api/categories")

categories = [
    { "id": 1, "name": "Beverages" },
    { "id": 2, "name": "Condiments" },
    { "id": 3, "name": "Produce" }
]

@cat_bp.get("/")
def handle_get_all():
    return jsonify(categories)

@cat_bp.post("/")
def handle_post():
    data = request.get_json()
    cat_name = data.get("name")
    if not cat_name:
        return jsonify({"error": "`name` is missing"}), 400
    
    new_cat_id = 1 + max([c.get("id") for c in categories])
    new_cat = {"id": new_cat_id, "name": cat_name}
    categories.append(new_cat)
    return jsonify(new_cat), 201
