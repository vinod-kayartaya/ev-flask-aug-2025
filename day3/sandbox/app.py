from flask import Flask, request, Response
import json
from dao import Book, BookJsonEncoder, add_book, get_all, get_by_id
from datetime import datetime
from flask_cors import CORS

app = Flask('Book Service')
CORS(app)

def create_response(data, status=200):
    return Response(json.dumps(data, cls=BookJsonEncoder), \
                    status=status, \
                        mimetype="application/json")

def create_error(message, status=400):
    err = {"message": message, "timestamp": str(datetime.now())}
    return Response(json.dumps(err), status=status, mimetype="application/json")

@app.get("/api/books")
def handle_get_all():
    all_books = get_all()
    return create_response(all_books)

@app.get("/api/books/<int:book_id>")
def handle_get_one(book_id):
    book = get_by_id(book_id)
    if book:
        return create_response(book)
    return create_error(f'no book found for id {book_id}', 404)


@app.post("/api/books")
def handle_post():
    data = request.get_json()
    book = Book(**data)
    book = add_book(book)
    return create_response(book, 201)


app.run(host="0.0.0.0", port=8080, debug=True)
