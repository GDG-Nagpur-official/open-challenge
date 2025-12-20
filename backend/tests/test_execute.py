import pytest
import requests
from unittest.mock import MagicMock
from bson import ObjectId

def test_execute_api_success(client, mock_db, auth_header, mocker):
    """Test execution of a proxy API request"""
    # Mock finding the API
    api_id = '507f1f77bcf86cd799439011'
    user_id = auth_header['user_id']
    mock_api = {
        '_id': ObjectId(api_id),
        'user_id': ObjectId(user_id),
        'endpoint': 'http://external-api.com/data',
        'method': 'GET',
        'headers': {},
        'body': {},
        'status': 'active'
    }
    mock_db['apis'].find_one.return_value = mock_api
    
    # Mock API Key validation
    mock_db['api_keys'].find_one.return_value = {
        'key': 'test_key',
        'is_active': True,
        'user_id': ObjectId(user_id)
    }
    
    # Mock external request
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': 'external result'}
    mock_response.headers = {'Content-Type': 'application/json'}
    
    mocker.patch('requests.request', return_value=mock_response)
    
    response = client.post(f'/api/execute/{api_id}', headers={'X-API-Key': 'test_key'})
    
    assert response.status_code == 200
    mock_db['logs'].insert_one.assert_called_once()

def test_execute_api_not_found(client, mock_db, mocker):
    """Test execution of non-existent API"""
    mock_db['apis'].find_one.return_value = None
    # Assuming utils.api_key_required still works, so we need a valid key first
    mock_db['api_keys'].find_one.return_value = {'key': 'key', 'is_active': True, 'user_id': ObjectId()}
    
    response = client.post('/api/execute/507f1f77bcf86cd799439011', headers={'X-API-Key': 'key'})
    
    assert response.status_code == 404

def test_execute_api_inactive(client, mock_db, mocker):
    """Test execution of inactive API"""
    mock_api = {
        '_id': ObjectId('507f1f77bcf86cd799439011'),
        'status': 'inactive',
        'user_id': ObjectId()
    }
    mock_db['apis'].find_one.return_value = mock_api
    mock_db['api_keys'].find_one.return_value = {'key': 'key', 'is_active': True, 'user_id': ObjectId()}
    
    response = client.post('/api/execute/507f1f77bcf86cd799439011', headers={'X-API-Key': 'key'})
    
    # Controller returns 403 for inactive
    assert response.status_code == 403

def test_execute_api_timeout(client, mock_db, mocker):
    """Test execution timeout handling"""
    mock_api = {
        '_id': ObjectId('507f1f77bcf86cd799439011'),
        'user_id': ObjectId(),
        'endpoint': 'http://timeout.com',
        'method': 'GET',
        'status': 'active'
    }
    mock_db['apis'].find_one.return_value = mock_api
    mock_db['api_keys'].find_one.return_value = {'key': 'key', 'is_active': True, 'user_id': ObjectId()}
    
    mocker.patch('requests.request', side_effect=requests.exceptions.Timeout)
    
    response = client.post('/api/execute/507f1f77bcf86cd799439011', headers={'X-API-Key': 'key'})
    
    assert response.status_code == 408
    # Log should record error
    mock_db['logs'].insert_one.assert_called_once()
    assert mock_db['logs'].insert_one.call_args[0][0]['error'] == 'Request timeout'

def test_execute_api_exception(client, mock_db, mocker):
    """Test execution general exception handling"""
    mock_api = {
        '_id': ObjectId('507f1f77bcf86cd799439011'),
        'user_id': ObjectId(),
        'endpoint': 'http://error.com',
        'method': 'GET',
        'status': 'active'
    }
    mock_db['apis'].find_one.return_value = mock_api
    mock_db['api_keys'].find_one.return_value = {'key': 'key', 'is_active': True, 'user_id': ObjectId()}
    
    mocker.patch('requests.request', side_effect=Exception('Unexpected error'))
    
    response = client.post('/api/execute/507f1f77bcf86cd799439011', headers={'X-API-Key': 'key'})
    
    assert response.status_code == 500
    assert 'Unexpected error' in response.json['error']
