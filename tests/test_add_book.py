def test_add_book_success(client):
    new_book = {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '978-0-000-00000-0'
    }
    response = client.post('/api/add', json=new_book)
    assert response.status_code == 201
    assert response.json['success'] is True
    assert 'Test Book' in response.json['message']
    assert response.json['book']['status'] == 'available'

def test_add_book_missing_fields(client):
    incomplete_book = {'title': 'Test Book'}
    response = client.post('/api/add', json=incomplete_book)
    assert response.status_code == 400
    assert response.json['success'] is False