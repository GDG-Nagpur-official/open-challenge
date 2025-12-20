import pytest
from unittest.mock import MagicMock
from bson import ObjectId

def test_get_apis(client, mock_db, auth_header):
    """Test retrieving user's APIs"""
    mock_apis = [
        {
            '_id': ObjectId('507f1f77bcf86cd799439011'),
            'name': 'Test API',
            'endpoint': 'http://example.com',
            'method': 'GET',
            'description': 'A test API',
            'headers': {},
            'body': {},
            'user_id': ObjectId(auth_header['user_id']),
            'created_at': '2024-01-01'
        }
    ]
    
    mock_cursor = MagicMock()
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.__iter__.return_value = iter(mock_apis)
    
    mock_db['apis'].find.return_value = mock_cursor
    mock_db['apis'].count_documents.return_value = 1
    
    response = client.get('/api/apis', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert len(response.json['apis']) == 1
    assert response.json['apis'][0]['name'] == 'Test API'

def test_get_api_detail(client, mock_db, auth_header):
    """Test retrieving single API detail"""
    api_id = '507f1f77bcf86cd799439011'
    mock_api = {'_id': ObjectId(api_id), 'user_id': ObjectId(auth_header['user_id']), 'name': 'Detail API'}
    mock_db['apis'].find_one.return_value = mock_api
    
    response = client.get(f'/api/apis/{api_id}', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert response.json['api']['name'] == 'Detail API'

def test_get_api_not_found(client, mock_db, auth_header):
    """Test retrieving non-existent API"""
    mock_db['apis'].find_one.return_value = None
    response = client.get('/api/apis/507f1f77bcf86cd799439011', headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 404
    assert 'error' in response.json

def test_get_api_invalid_id(client, mock_db, auth_header):
    """Test retrieving API with invalid ID format"""
    response = client.get('/api/apis/invalid-id', headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 400
    assert 'error' in response.json

def test_create_api(client, mock_db, auth_header):
    """Test creating a new API"""
    mock_db['apis'].insert_one.return_value = MagicMock(inserted_id=ObjectId('507f1f77bcf86cd799439011'))
    
    data = {
        'name': 'New API',
        'endpoint': 'http://newapi.com',
        'method': 'POST',
        'description': 'New Description'
    }
    
    response = client.post('/api/apis', json=data, headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 201
    assert response.json['message'] == 'API created successfully'
    mock_db['apis'].insert_one.assert_called_once()

def test_create_api_missing_fields(client, mock_db, auth_header):
    """Test creation with missing required fields"""
    data = {'name': 'New API'} # Missing endpoint
    response = client.post('/api/apis', json=data, headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 400
    assert 'error' in response.json

def test_create_api_invalid_method(client, mock_db, auth_header):
    """Test creation with invalid HTTP method"""
    data = {
        'name': 'New API', 
        'endpoint': 'http://example.com',
        'method': 'INVALID'
    }
    response = client.post('/api/apis', json=data, headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 400
    assert 'error' in response.json

def test_update_api(client, mock_db, auth_header):
    """Test updating an existing API"""
    api_id = '507f1f77bcf86cd799439011'
    
    # Mock finding the API (ownership check)
    mock_api = {'_id': ObjectId(api_id), 'user_id': ObjectId(auth_header['user_id']), 'name': 'Old Name'}
    # First find_one is for check, second find_one is for fetching updated doc
    mock_db['apis'].find_one.side_effect = [mock_api, {**mock_api, 'name': 'Updated API Name'}]
    
    mock_db['apis'].update_one.return_value = MagicMock(matched_count=1)
    
    data = {
        'name': 'Updated API Name'
    }
    
    response = client.put(f'/api/apis/{api_id}', json=data, headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert response.json['message'] == 'API updated successfully'
    assert response.json['api']['name'] == 'Updated API Name'

def test_update_api_invalid_id(client, mock_db, auth_header):
    """Test updating API with invalid ID"""
    response = client.put('/api/apis/invalid-id', json={'name': 'New'}, headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 400
    assert 'error' in response.json

def test_update_api_not_found(client, mock_db, auth_header):
    """Test updating non-existent API"""
    mock_db['apis'].find_one.return_value = None
    response = client.put('/api/apis/507f1f77bcf86cd799439011', json={'name': 'New'}, headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 404
    assert 'error' in response.json

def test_update_api_invalid_method(client, mock_db, auth_header):
    """Test updating API with invalid method"""
    api_id = '507f1f77bcf86cd799439011'
    mock_api = {'_id': ObjectId(api_id), 'user_id': ObjectId(auth_header['user_id'])}
    mock_db['apis'].find_one.return_value = mock_api
    
    response = client.put(f'/api/apis/{api_id}', json={'method': 'INVALID'}, headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 400
    assert 'error' in response.json

def test_delete_api(client, mock_db, auth_header):
    """Test deleting an API"""
    api_id = '507f1f77bcf86cd799439011'
    # Mock finding the API (ownership check)
    mock_db['apis'].find_one.return_value = {'_id': ObjectId(api_id), 'user_id': ObjectId(auth_header['user_id'])}
    
    mock_db['apis'].delete_one.return_value = MagicMock(deleted_count=1)
    
    response = client.delete(f'/api/apis/{api_id}', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert response.json['message'] == 'API deleted successfully'

def test_delete_api_invalid_id(client, mock_db, auth_header):
    """Test deleting API with invalid ID"""
    response = client.delete('/api/apis/invalid-id', headers={'Authorization': auth_header['Authorization']})
    assert response.status_code == 400
    assert 'error' in response.json

def test_delete_api_not_found(client, mock_db, auth_header):
    """Test deleting a non-existent API"""
    api_id = '507f1f77bcf86cd799439011'
    # Mock finding the API (returns None)
    mock_db['apis'].find_one.return_value = None
    
    mock_db['apis'].delete_one.return_value = MagicMock(deleted_count=0)
    
    response = client.delete(f'/api/apis/{api_id}', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 404
