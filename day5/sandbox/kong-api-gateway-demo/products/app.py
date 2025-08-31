from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/products")
def get_products():
    return jsonify([
        {"id": 1, "name": "Laptop", "price": 50000},
        {"id": 2, "name": "Mobile", "price": 20000}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6010)