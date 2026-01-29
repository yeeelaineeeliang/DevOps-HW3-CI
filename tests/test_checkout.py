def test_checkout_available_book(client, sample_inventory):
    response = client.post("/api/checkout", json={"isbn": "978-0-7432-7356-5"})
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["book"]["status"] == "checked_out"


def test_checkout_already_checked_out(client, sample_inventory):
    # First checkout
    client.post("/api/checkout", json={"isbn": "978-0-7432-7356-5"})
    # Try to checkout again
    response = client.post("/api/checkout", json={"isbn": "978-0-7432-7356-5"})
    assert response.status_code == 400
    assert response.json["success"] is False


def test_checkout_nonexistent_book(client):
    response = client.post("/api/checkout", json={"isbn": "978-9999-9999-9"})
    assert response.status_code == 400
    assert response.json["success"] is False
