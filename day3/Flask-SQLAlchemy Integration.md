# Flask-SQLAlchemy Integration

Flask is one of the most popular microframeworks in Python, known for its simplicity and flexibility. While Flask is great for building web applications, most real-world projects need to **persist data** in a database. This is where **SQLAlchemy** comes into play — it provides a powerful and Pythonic way to interact with databases.

In this blog post, we’ll walk through how to integrate **Flask with SQLAlchemy**, set up a simple application, and perform CRUD (Create, Read, Update, Delete) operations using Indian data samples.

---

## 🔹 Why SQLAlchemy with Flask?

* **ORM (Object Relational Mapper):** SQLAlchemy allows you to work with Python objects instead of writing raw SQL queries.
* **Database Flexibility:** Works with multiple databases (MySQL, PostgreSQL, SQLite, etc.).
* **Ease of Integration:** Flask-SQLAlchemy extension makes it seamless to use with Flask apps.

---

## 🔹 Setting Up the Project

### 1. Install Flask and Flask-SQLAlchemy

```bash
pip install flask flask_sqlalchemy
```

### 2. Create Project Structure

```
flask_sqlalchemy_demo/
│── app.py
│── models.py
│── database.db
```

---

## 🔹 Step 1: Initialize Flask with SQLAlchemy

**app.py**

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite Database (can be replaced with MySQL/PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

---

## 🔹 Step 2: Define Models

We’ll create two models:

* **State** → Represents Indian states
* **City** → Represents cities belonging to a state

**models.py**

```python
from app import db

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    capital = db.Column(db.String(100), nullable=False)

    cities = db.relationship('City', backref='state', lazy=True)

    def __repr__(self):
        return f"<State {self.name}>"

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer, nullable=False)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __repr__(self):
        return f"<City {self.name}>"
```

Now, let’s create the database.

---

## 🔹 Step 3: Create Database

Open Python shell:

```bash
python
```

```python
from app import db
import models

db.create_all()
```

This will generate a **database.db** SQLite file with `states` and `cities` tables.

---

## 🔹 Step 4: Insert Sample Indian Data

We’ll insert data for a few states and cities.

```python
from models import State, City
from app import db

# Create States
karnataka = State(name="Karnataka", capital="Bengaluru")
maharashtra = State(name="Maharashtra", capital="Mumbai")

db.session.add(karnataka)
db.session.add(maharashtra)
db.session.commit()

# Create Cities
bengaluru = City(name="Bengaluru", population=8443675, state=karnataka)
mysuru = City(name="Mysuru", population=920550, state=karnataka)
mumbai = City(name="Mumbai", population=12442373, state=maharashtra)
pune = City(name="Pune", population=3124458, state=maharashtra)

db.session.add_all([bengaluru, mysuru, mumbai, pune])
db.session.commit()
```

---

## 🔹 Step 5: Expose REST APIs

Now, let’s create endpoints to perform CRUD operations.

**app.py (continued)**

```python
from models import State, City, db

# Home Route
@app.route('/')
def home():
    return "Welcome to Flask-SQLAlchemy Demo with Indian Data"

# Get all states
@app.route('/states')
def get_states():
    states = State.query.all()
    return jsonify([{"id": s.id, "name": s.name, "capital": s.capital} for s in states])

# Get all cities for a state
@app.route('/states/<int:state_id>/cities')
def get_cities(state_id):
    cities = City.query.filter_by(state_id=state_id).all()
    return jsonify([{"id": c.id, "name": c.name, "population": c.population} for c in cities])

# Add a new state
@app.route('/state', methods=['POST'])
def add_state():
    data = request.json
    new_state = State(name=data['name'], capital=data['capital'])
    db.session.add(new_state)
    db.session.commit()
    return jsonify({"message": "State added successfully!"})
```

---

## 🔹 Step 6: Test the APIs

### ✅ Fetch All States

```bash
curl http://127.0.0.1:5000/states
```

**Response:**

```json
[
  {"id": 1, "name": "Karnataka", "capital": "Bengaluru"},
  {"id": 2, "name": "Maharashtra", "capital": "Mumbai"}
]
```

### ✅ Fetch Cities of Karnataka

```bash
curl http://127.0.0.1:5000/states/1/cities
```

**Response:**

```json
[
  {"id": 1, "name": "Bengaluru", "population": 8443675},
  {"id": 2, "name": "Mysuru", "population": 920550}
]
```

### ✅ Insert a New State

```bash
curl -X POST http://127.0.0.1:5000/state \
-H "Content-Type: application/json" \
-d '{"name": "Tamil Nadu", "capital": "Chennai"}'
```

**Response:**

```json
{"message": "State added successfully!"}
```

---

## 🔹 Step 7: Update and Delete

```python
# Update a state
@app.route('/state/<int:id>', methods=['PUT'])
def update_state(id):
    data = request.json
    state = State.query.get_or_404(id)
    state.name = data['name']
    state.capital = data['capital']
    db.session.commit()
    return jsonify({"message": "State updated successfully!"})

# Delete a state
@app.route('/state/<int:id>', methods=['DELETE'])
def delete_state(id):
    state = State.query.get_or_404(id)
    db.session.delete(state)
    db.session.commit()
    return jsonify({"message": "State deleted successfully!"})
```

---

## 🔹 Step 8: Run the App

```bash
python app.py
```

Now open `http://127.0.0.1:5000` in your browser.

---

## 🔹 Conclusion

We’ve successfully built a **Flask + SQLAlchemy application** that:
✅ Defines models for Indian states and cities
✅ Performs CRUD operations
✅ Exposes REST APIs
✅ Uses SQLite for simplicity (can easily switch to MySQL/PostgreSQL)

This tutorial demonstrates the ease of integrating Flask with SQLAlchemy for real-world projects. You can extend this further to include **relationships, authentication, pagination, or even deploy it with Docker**.

---

👉 Next steps:

* Try adding **districts** under states
* Implement search functionality (e.g., find cities above 1 million population)
* Secure APIs with **Flask-JWT-Extended**

---
