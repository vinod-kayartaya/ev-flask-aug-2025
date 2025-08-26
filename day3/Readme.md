# Flask-SQLAlchemy Integration

Most modern applications need a backend that can manage **structured data** efficiently — products, users, orders, categories, and so on. Flask, with its minimalistic approach, makes a great choice for building such applications. Combined with **SQLAlchemy** (ORM for Python), you can manage database interactions cleanly without writing raw SQL all the time.

In this step-by-step guide, we’ll build a **Flask + SQLAlchemy application** that manages **Products and Categories** with support for:

- Models and relationships (One-to-Many, Many-to-Many)
- Migration management with **Flask-Migrate**
- Query optimization
- Role-Based Access Control (RBAC) strategies

We’ll use **products** as examples, so the data feels familiar and practical.

---

## 🔹 Step 1: Setup the Environment

Install required packages:

```bash
pip install flask flask_sqlalchemy flask_migrate flask-bcrypt flask-jwt-extended
```

Project structure:

```
flask_sqlalchemy_products/
│── app.py
│── models.py
│── routes.py
│── config.py
│── migrations/
│── database.db
```

---

## 🔹 Step 2: Configure Flask and Database

**config.py**

```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey"
```

**app.py**

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from routes import main
    app.register_blueprint(main)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 🔹 Step 3: Define Models & Relationships

We’ll have:

- **Category** (e.g., Electronics, Groceries)
- **Product** (belongs to one category, can have multiple tags)
- **Tag** (Many-to-Many relationship with Products)
- **User** (with roles for RBAC: admin, manager, customer)

**models.py**

```python
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Association table for Many-to-Many
product_tags = db.Table('product_tags',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tags = db.relationship('Tag', secondary=product_tags, lazy='subquery',
                           backref=db.backref('products', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="customer")  # admin, manager, customer

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
```

---

## 🔹 Step 4: Database Migrations with Flask-Migrate

Instead of manually creating tables, we’ll use **Flask-Migrate**.

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

This will generate versioned migrations inside the **migrations/** folder.

Now you can evolve your database schema safely over time.

---

## 🔹 Step 5: Add Routes for CRUD Operations

**routes.py**

```python
from flask import Blueprint, request, jsonify
from app import db
from models import Category, Product, Tag, User

main = Blueprint('main', __name__)

# Create a category
@main.route('/category', methods=['POST'])
def create_category():
    data = request.json
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created"})

# Get categories with products (optimized query)
@main.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.options(db.joinedload(Category.products)).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "products": [{"id": p.id, "name": p.name, "price": p.price} for p in c.products]
        }
        for c in categories
    ])

# Add a product with category & tags
@main.route('/product', methods=['POST'])
def create_product():
    data = request.json
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({"error": "Category not found"}), 404

    product = Product(
        name=data['name'],
        price=data['price'],
        stock=data.get('stock', 0),
        category=category
    )

    if 'tags' in data:
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            product.tags.append(tag)

    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"})
```

---

## 🔹 Step 6: Insert sample Data

```bash
curl -X POST http://127.0.0.1:5000/category \
-H "Content-Type: application/json" \
-d '{"name": "Electronics"}'

curl -X POST http://127.0.0.1:5000/product \
-H "Content-Type: application/json" \
-d '{"name": "Mi LED TV", "price": 32999, "stock": 25, "category_id": 1, "tags": ["TV", "Smart"]}'
```

We now have **Electronics → Mi LED TV (tags: TV, Smart)**.
You can add more: `"Tata Salt"`, `"Amul Butter"`, `"Samsung Galaxy S23"` etc.

---

## 🔹 Step 7: Query Optimization

Instead of multiple queries (N+1 problem), use:

```python
from sqlalchemy.orm import joinedload

categories = Category.query.options(joinedload(Category.products)).all()
```

This fetches **categories and products in one go**, improving performance.

Other strategies:

- Use `.with_entities()` to fetch only required columns.
- Use `.filter_by()` and `.filter()` with indexes.
- Apply pagination (`.limit().offset()`).

---

## 🔹 Step 8: Role-Based Access Control (RBAC)

We’ll keep RBAC simple:

- **Admin:** Can create categories/products, delete anything
- **Manager:** Can update stock/prices
- **Customer:** Can only view products

Example check:

```python
def check_role(user, required_role):
    roles = {"admin": 3, "manager": 2, "customer": 1}
    return roles[user.role] >= roles[required_role]

@main.route('/secure-add-product', methods=['POST'])
def secure_add_product():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Unauthorized"}), 401

    if not check_role(user, "admin"):
        return jsonify({"error": "Permission denied"}), 403

    # proceed with product creation...
    return jsonify({"message": "Product added securely!"})
```

This way, **only admins** can add products, while managers and customers have restricted privileges.

---

## 🔹 Step 9: Run the App

```bash
python app.py
```

Open: [http://127.0.0.1:5000/categories](http://127.0.0.1:5000/categories)

---

## 🔹 Conclusion

In this tutorial, we’ve covered:

✅ Setting up Flask with SQLAlchemy
✅ Defining models with **1-to-Many & Many-to-Many relationships**
✅ Managing schema changes with **Flask-Migrate**
✅ Optimizing queries for better performance
✅ Implementing a simple **RBAC strategy**

This provides a **production-ready foundation** for an e-commerce or inventory management system with **Products & Categories**.

---

👉 Next Steps:

- Add **JWT-based authentication** using `flask-jwt-extended`
- Add **pagination & sorting** for large product lists
- Add **unit tests** for APIs
