import pytest
from unittest.mock import MagicMock
from bson import ObjectId

def test_get_api_keys(client, mock_db, auth_header):
    """Test retrieving user's API keys"""
    mock_keys = [
        {
            '_id': ObjectId('507f1f77bcf86cd799439011'),
            'key': 'test_api_key_123',
            'name': 'Default Key',
            'user_id': ObjectId(auth_header['user_id']),
            'created_at': '2024-01-01'
        }
    ]
    
    mock_cursor = MagicMock()
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.__iter__.return_value = iter(mock_keys)
    
    # Configure the mock to return the cursor
    mock_db['api_keys'].find.return_value = mock_cursor
    
    response = client.get('/api/keys', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert len(response.json['keys']) == 1
    assert response.json['keys'][0]['name'] == 'Default Key'

def test_create_api_key(client, mock_db, auth_header):
    """Test creating a new API key"""
    mock_db['api_keys'].find_one.return_value = None # No existing key collision
    mock_db['api_keys'].insert_one.return_value = MagicMock(inserted_id=ObjectId('507f1f77bcf86cd799439011'))
    
    data = {'name': 'New Key'}
    
    response = client.post('/api/keys', json=data, headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 201
    assert 'key' in response.json
    mock_db['api_keys'].insert_one.assert_called_once()

def test_revoke_api_key(client, mock_db, auth_header):
    """Test revoking (deleting) an API key"""
    # Mock finding the key first (required by logic)
    mock_db['api_keys'].find_one.return_value = {'_id': ObjectId('507f1f77bcf86cd799439011')}
    mock_db['api_keys'].delete_one.return_value = MagicMock(deleted_count=1)
    
    key_id = '507f1f77bcf86cd799439011'
    response = client.delete(f'/api/keys/{key_id}', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert response.json['message'] == 'API key deleted successfully'
