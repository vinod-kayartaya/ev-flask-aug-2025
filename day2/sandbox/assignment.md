# Assignment: Extend `/api/customers/<id>` with PUT, PATCH, and DELETE

## Objective

The current `main.py` implements a simple customer management API with **`GET`** and **`POST`** endpoints.
Your task is to extend this service by implementing **`PUT`**, **`PATCH`**, and **`DELETE`** methods for `/api/customers/<id>`.

---

## Tasks

### 1. PUT Request – Replace a Customer

- Add a route for `PUT /api/customers/<uuid:customer_id>`.
- Expected behavior:

  - If the customer exists → replace all fields with the new data.
  - If the customer does not exist → return `404 Not Found`.
  - Validate fields (same as `POST`):

    - Required: `name`, `email`, `phone`.
    - Email must be valid (`email_validator`).
    - Phone and email must be unique.

- Response codes:

  - `200 OK` → Successfully updated.
  - `400 Bad Request` → Validation failed.
  - `404 Not Found` → Customer not found.

---

### 2. PATCH Request – Partially Update a Customer

- Add a route for `PATCH /api/customers/<uuid:customer_id>`.
- Expected behavior:

  - Only update fields provided in the request body.
  - If customer does not exist → return `404 Not Found`.
  - Validation:

    - If `email` is provided, it must be valid and unique.
    - If `phone` is provided, it must be unique.

- Response codes:

  - `200 OK` → Successfully updated.
  - `400 Bad Request` → Validation failed.
  - `404 Not Found` → Customer not found.

---

### 3. DELETE Request – Remove a Customer

- Add a route for `DELETE /api/customers/<uuid:customer_id>`.
- Expected behavior:

  - If customer exists → delete it from `_customers` and update `customers.json`.
  - If customer does not exist → return `404 Not Found`.

- Response codes:

  - `204 No Content` → Successfully deleted.
  - `404 Not Found` → Customer not found.

---

## Validation Rules

Follow the same rules already present in `handle_post`:

- `name`, `email`, `phone` are required (for `PUT`).
- `email` must be valid and unique.
- `phone` must be unique.
- For `PATCH`, only validate the fields being updated.

---

## Test Requests (`test-requests.http`)

Extend your existing `test-requests.http` with:

### PUT Example

```http
PUT http://localhost:5002/api/customers/238fa401-bc28-4a19-96b8-394e1da0c42e
Content-Type: application/json

{
  "name": "Rajesh Kumar",
  "email": "rajesh.kumar@example.com",
  "phone": "919876543210",
  "gender": "Male",
  "address": "7th cross, 8th main, JP nagar",
  "city": "Bengaluru",
  "country": "India"
}
```

### PATCH Example

```http
PATCH http://localhost:5002/api/customers/238fa401-bc28-4a19-96b8-394e1da0c42e
Content-Type: application/json

{
  "email": "rajesh_kumar_2233@example.com"
}
```

### DELETE Example

```http
DELETE http://localhost:5002/api/customers/238fa401-bc28-4a19-96b8-394e1da0c42e
```

_(Replace the UUID with one from your `customers.json` file.)_
