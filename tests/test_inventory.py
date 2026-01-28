def test_get_inventory_returns_books(client, sample_inventory):
    response = client.get('/api/inventory')
    assert response.status_code == 200
    assert 'books' in response.json
    assert 'total_books' in response.json
    assert 'available' in response.json
    assert 'checked_out' in response.json
    assert response.json['total_books'] >= 0