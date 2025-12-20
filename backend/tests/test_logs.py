import pytest
from unittest.mock import MagicMock
from bson import ObjectId

def test_get_logs(client, mock_db, auth_header):
    """Test retrieving activity logs"""
    mock_logs = [
        {
            '_id': ObjectId('507f1f77bcf86cd799439011'),
            'api_id': ObjectId('507f1f77bcf86cd799439011'),
            'status': 200,
            'response_time': 0.1,
            'timestamp': '2024-01-01'
        }
    ]
    
    # Mock cursor for find() chain used in logs.py
    mock_cursor = MagicMock()
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.__iter__.return_value = iter(mock_logs)

    mock_db['logs'].find.return_value = mock_cursor
    mock_db['logs'].count_documents.return_value = 1
    
    response = client.get('/api/logs', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert 'logs' in response.json
    assert isinstance(response.json['logs'], list)

def test_get_stats(client, mock_db, auth_header):
    """Test retrieving log statistics"""
    # Mock counts: total, success (2xx), error (4xx)
    mock_db['logs'].count_documents.side_effect = [100, 80, 20]
    
    # Mock aggregation for avg response time
    mock_db['logs'].aggregate.return_value = [{'avg_response_time': 123.45}]
    # Note: aggregate returns a cursor/iterator, usually list() is called on it.
    # If the code calls list(collection.aggregate(...)), return_value needs to be iterable.
    # But often mock return_value as list works if iterated.
    
    response = client.get('/api/logs/stats', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    stats = response.json
    assert stats['total_requests'] == 100
    assert stats['success_requests'] == 80
    assert stats['error_requests'] == 20
    assert stats['avg_response_time'] == 123.45
