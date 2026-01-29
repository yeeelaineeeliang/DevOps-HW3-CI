def test_health_structure(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "inventory_count" in data


def test_inventory_structure_keys(client):
    resp = client.get("/api/inventory")
    assert resp.status_code == 200
    data = resp.get_json()
    for k in ["total_books", "available", "checked_out", "books"]:
        assert k in data


def test_add_book_success_returns_201(client):
    resp = client.post(
        "/api/add",
        json={"title": "Dune", "author": "Frank Herbert", "isbn": "9780441013593"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"] is True
    assert data["book"]["isbn"] == "9780441013593"


def test_add_book_missing_field_returns_400(client):
    resp = client.post("/api/add", json={"title": "Dune", "author": "Frank Herbert"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False


def test_search_missing_query_returns_400(client):
    resp = client.post("/api/commands/search", json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False


def test_search_empty_query_returns_200(client):
    resp = client.post("/api/commands/search", json={"query": ""})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert isinstance(data["count"], int)


def test_checkout_missing_isbn_returns_400(client):
    resp = client.post("/api/commands/checkout", json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False


def test_checkout_nonexistent_returns_400(client):
    resp = client.post("/api/commands/checkout", json={"isbn": "0000000000"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False


def test_checkout_then_return_happy_path(client):
    # add
    client.post(
        "/api/add",
        json={"title": "Dune", "author": "Frank Herbert", "isbn": "9780441013593"},
    )

    # checkout
    r_checkout = client.post("/api/commands/checkout", json={"isbn": "9780441013593"})
    assert r_checkout.status_code == 200
    d_checkout = r_checkout.get_json()
    assert d_checkout["success"] is True
    assert d_checkout["book"]["status"] == "checked_out"

    # return
    r_return = client.post("/api/commands/return", json={"isbn": "9780441013593"})
    assert r_return.status_code == 200
    d_return = r_return.get_json()
    assert d_return["success"] is True
    assert d_return["book"]["status"] == "available"


def test_return_nonexistent_returns_404(client):
    resp = client.post("/api/commands/return", json={"isbn": "0000000000"})
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["success"] is False


def test_remove_nonexistent_returns_404(client):
    resp = client.post("/api/commands/remove", json={"isbn": "0000000000"})
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["success"] is False


def test_remove_happy_path(client):
    client.post(
        "/api/add",
        json={"title": "Dune", "author": "Frank Herbert", "isbn": "9780441013593"},
    )
    resp = client.post("/api/commands/remove", json={"isbn": "9780441013593"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
