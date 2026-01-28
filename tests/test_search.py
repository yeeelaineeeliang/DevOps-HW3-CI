def test_search_by_author(client, sample_inventory):
    response = client.post('/api/search', json={'query': 'orwell'})
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['count'] >= 1
    assert any('Orwell' in book['author'] for book in response.json['results'])

def test_search_by_title(client, sample_inventory):
    response = client.post('/api/search', json={'query': 'gatsby'})
    assert response.status_code == 200
    assert response.json['count'] >= 1

def test_search_no_results(client, sample_inventory):
    response = client.post('/api/search', json={'query': 'nonexistent'})
    assert response.status_code == 200
    assert response.json['count'] == 0
    assert response.json['results'] == []