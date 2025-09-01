from flask import Flask, jsonify

app = Flask(__name__)


_customers = [
        {"id": 1, "name": "Vinod", "city": "Bangalore", "email": "vinod@vinod.co", "phone": "9731424784"},
        {"id": 2, "name": "John", "city": "Delhi", "email": "john@example.com", "phone": "9812345678"}
    ]

@app.route("/api/customers")
def get_customers():
    return jsonify(_customers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6020)