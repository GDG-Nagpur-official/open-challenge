import pytest
import sys
import os
from unittest.mock import MagicMock

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def mock_db(mocker):
    # Create mock collections
    mock_users = MagicMock()
    mock_apis = MagicMock()
    mock_api_keys = MagicMock()
    mock_logs = MagicMock()
    
    # Patch in database module (base)
    mocker.patch('database.users_collection', mock_users)
    mocker.patch('database.apis_collection', mock_apis)
    mocker.patch('database.api_keys_collection', mock_api_keys)
    mocker.patch('database.logs_collection', mock_logs)
    
    # Patch in route modules (where they are imported from database)
    # We catch generic import errors just in case, but usually we want to know.
    # Actually, removing try/except to see if it fails.
    
    mocker.patch('routes.auth.users_collection', mock_users)
    mocker.patch('routes.apis.apis_collection', mock_apis)
    mocker.patch('routes.api_keys.api_keys_collection', mock_api_keys)
    mocker.patch('routes.logs.logs_collection', mock_logs)
    mocker.patch('routes.execute.apis_collection', mock_apis)
    mocker.patch('routes.execute.logs_collection', mock_logs)
    mocker.patch('utils.api_keys_collection', mock_api_keys)
    
    return {
        'users': mock_users,
        'apis': mock_apis,
        'api_keys': mock_api_keys,
        'logs': mock_logs
    }

@pytest.fixture
def auth_header(client, mock_db):
    # Helper to generate a valid auth header for a mock user
    from flask_jwt_extended import create_access_token
    
    user_id = "507f1f77bcf86cd799439011"
    with flask_app.app_context():
        token = create_access_token(identity=user_id)
        
    return {
        'Authorization': f'Bearer {token}', 
        'user_id': user_id
    }
