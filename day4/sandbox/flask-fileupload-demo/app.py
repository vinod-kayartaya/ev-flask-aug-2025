import os
from uuid import uuid4
from flask import Flask, request, jsonify, send_from_directory, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# -------------------
# App configuration
# -------------------
app = Flask(__name__)

# SQLite DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# File upload settings
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB max
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)

# -------------------
# Model
# -------------------
class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    photo_filename = db.Column(db.String(255))        # stored filename on disk
    photo_original_name = db.Column(db.String(255))   # original upload name (for reference)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "email": self.email,
            "phone": self.phone,
            "photo_url": url_for("get_customer_photo", id=self.id, _external=True) if self.photo_filename else None,
        }

# -------------------
# Helpers
# -------------------
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_photo(file_storage):
    """
    Validates & saves an uploaded photo.
    Returns (stored_filename, original_filename).
    """
    if file_storage and file_storage.filename:
        original_name = secure_filename(file_storage.filename)
        if not allowed_file(original_name):
            abort(400, description="Invalid file type. Allowed: png, jpg, jpeg, gif")
        ext = os.path.splitext(original_name)[1].lower()
        stored_name = f"{uuid4().hex}{ext}"  # avoid collisions
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
        file_storage.save(save_path)
        return stored_name, original_name
    return None, None

def delete_photo_if_exists(stored_filename):
    if not stored_filename:
        return
    path = os.path.join(app.config["UPLOAD_FOLDER"], stored_filename)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        # In real apps, log this
        pass

# -------------------
# Routes
# -------------------

@app.route("/api/customers", methods=["POST"])
def create_customer():
    """
    Create a customer (multipart/form-data).
    Fields: name, city, email, phone, photo (file)
    """
    # Validate form fields
    name = request.form.get("name")
    city = request.form.get("city")
    email = request.form.get("email")
    phone = request.form.get("phone")

    if not all([name, email, phone]):
        return jsonify({"error": "name, email and phone are required"}), 400

    # Check uniqueness for email/phone (simple check; database uniqueness enforces too)
    if Customer.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 409
    if Customer.query.filter_by(phone=phone).first():
        return jsonify({"error": "phone already exists"}), 409

    photo_file = request.files.get("photo")
    stored_name, original_name = save_uploaded_photo(photo_file)

    customer = Customer(
        name=name.strip(),
        city=(city or "").strip(),
        email=email.strip(),
        phone=phone.strip(),
        photo_filename=stored_name,
        photo_original_name=original_name,
    )
    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "created", "data": customer.to_dict()}), 201


@app.route("/api/customers", methods=["GET"])
def list_customers():
    customers = Customer.query.order_by(Customer.id).all()
    return jsonify({"data": [c.to_dict() for c in customers]}), 200


@app.route("/api/customers/<int:id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({"data": customer.to_dict()}), 200


@app.route("/api/customers/<int:id>", methods=["PUT", "PATCH"])
def update_customer(id):
    """
    Update basic fields and optionally replace photo.
    Accepts multipart/form-data to support new photo.
    """
    customer = Customer.query.get_or_404(id)

    # These may come from either form or JSON; we keep it consistent with form for file support.
    name = request.form.get("name")
    city = request.form.get("city")
    email = request.form.get("email")
    phone = request.form.get("phone")

    if email and Customer.query.filter(Customer.email == email, Customer.id != id).first():
        return jsonify({"error": "email already exists"}), 409
    if phone and Customer.query.filter(Customer.phone == phone, Customer.id != id).first():
        return jsonify({"error": "phone already exists"}), 409

    if name: customer.name = name.strip()
    if city is not None: customer.city = city.strip()
    if email: customer.email = email.strip()
    if phone: customer.phone = phone.strip()

    # Replace photo if provided
    photo_file = request.files.get("photo")
    if photo_file and photo_file.filename:
        stored_name, original_name = save_uploaded_photo(photo_file)
        # delete old
        delete_photo_if_exists(customer.photo_filename)
        customer.photo_filename = stored_name
        customer.photo_original_name = original_name

    db.session.commit()
    return jsonify({"message": "updated", "data": customer.to_dict()}), 200


@app.route("/api/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    delete_photo_if_exists(customer.photo_filename)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


@app.route("/api/customers/<int:id>/photo", methods=["GET"])
def get_customer_photo(id):
    """
    Serve the stored image file for a customer.
    """
    customer = Customer.query.get_or_404(id)
    if not customer.photo_filename:
        abort(404, description="No photo for this customer")
    return send_from_directory(app.config["UPLOAD_FOLDER"], customer.photo_filename)


# Initialize DB
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
