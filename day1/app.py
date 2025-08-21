from flask import Flask, request, Response
from data import _products
import json

app = Flask(__name__)

def product_to_text(p):
    if not p: return None

    return f'Product(id={p.get('id')}, name={p.get('name')}, price={p.get('price')}, category={p.get('category')})'

def products_to_text(products):
    return '\n'.join([product_to_text(p) for p in products])

def create_response(data=None, status=200):
    accept = request.headers["Accept"]
    if accept == "application/json":
        return Response(json.dumps(data), mimetype="application/json", status=status)
    elif accept == "text/plain":
        response_text = products_to_text(data) \
            if isinstance(data, list) \
            else product_to_text(data)
        return Response(response_text, mimetype="text/plain", status=status)
    else:
        status = 406

    return Response(None, status)



@app.get("/api/products")
def handle_get_products():
    return create_response(_products)


@app.get("/api/products/<int:p_id>")
def handle_get_one_product(p_id):

    data = [p for p in _products if p['id']==p_id]

    if len(data)==0:
        return create_response(None, status=404)

    return create_response(data[0])

@app.route("/")
def index():
    return "Hello, world!"

app.run(debug=True, host="0.0.0.0", port=5001)