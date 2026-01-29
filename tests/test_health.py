def test_health_endpoint_returns_200(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert "inventory_count" in response.json
