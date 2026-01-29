def test_health_ok(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"


def test_inventory_ok(client):
    resp = client.get("/api/inventory")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "books" in data


def test_add_book_success(client):
    resp = client.post(
        "/api/add",
        json={"title": "Dune", "author": "Frank Herbert", "isbn": "9780441013593"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"] is True


def test_add_book_missing_field_returns_400(client):
    resp = client.post("/api/add", json={"title": "Dune", "author": "Frank Herbert"})
    assert resp.status_code in (400, 422) 
    data = resp.get_json()
    assert data["success"] is False


def test_search_no_results(client):
    resp = client.post("/api/commands/search", json={"query": "NonexistentTitle"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["count"] == 0
