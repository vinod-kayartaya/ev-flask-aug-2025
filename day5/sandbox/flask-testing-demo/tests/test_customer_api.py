def test_create_customer(client):
    """Test POST /api/customers/"""
    response = client.post("/api/customers/", json={
        "name": "Vinod",
        "city": "Bangalore",
        "email": "vinod@vinod.co",
        "phone": "9731424784"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Vinod"
    assert data["email"] == "vinod@vinod.co"


def test_list_customers(client):
    """Test GET /api/customers/"""
    # First, create a customer
    client.post("/api/customers/", json={
        "name": "Vinod",
        "city": "Bangalore",
        "email": "vinod@vinod.co",
        "phone": "9731424784"
    })

    response = client.get("/api/customers/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["city"] == "Bangalore"