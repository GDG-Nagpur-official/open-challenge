import json
from unittest.mock import MagicMock
from bson import ObjectId
import pytest

def test_register_success(client, mock_db):
    """Test successful user registration"""
    mock_db['users'].find_one.return_value = None
    mock_db['users'].insert_one.return_value = MagicMock(inserted_id=ObjectId('507f1f77bcf86cd799439011'))
    
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/auth/register', json=data)
    
    assert response.status_code == 201
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json
    mock_db['users'].insert_one.assert_called_once()

def test_register_duplicate_user(client, mock_db):
    """Test registration with existing user"""
    mock_db['users'].find_one.return_value = {'_id': ObjectId('507f1f77bcf86cd799439011')}
    
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/auth/register', json=data)
    
    assert response.status_code == 409
    assert 'error' in response.json

def test_register_missing_fields(client, mock_db):
    """Test registration with missing fields"""
    data = {'username': 'testuser'} # Missing email and password
    response = client.post('/api/auth/register', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_register_invalid_email(client, mock_db):
    """Test registration with invalid email"""
    data = {
        'username': 'testuser',
        'email': 'not-an-email',
        'password': 'password123'
    }
    response = client.post('/api/auth/register', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_register_short_password(client, mock_db):
    """Test registration with short password"""
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': '123'
    }
    response = client.post('/api/auth/register', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_login_success(client, mock_db):
    """Test successful login"""
    # Mock user with hashed password (using a known hash for 'password123')
    # Use bcrypt to generate a real hash for mocking if needed, or mock the verify_password method.
    # Here we will rely on patching User.verify_password or just mocking the whole user object if logic permits.
    # Looking at auth.py: User.verify_password(user['password'], password)
    
    # Ideally we should mock the model method too, but for integration simplicity let's mock the DB return
    # and we depend on the real verify_password working if we provide a valid hash.
    # However, generating a hash in tests can be slow. Let's patch User.verify_password in the test if possible.
    
    # Creating a mock user object
    user_id = ObjectId('507f1f77bcf86cd799439011')
    mock_user = {
        '_id': user_id,
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'hashed_password_placeholder'
    }
    mock_db['users'].find_one.return_value = mock_user
    
    with pytest.MonkeyPatch.context() as mp:
        # Patch the User.verify_password method to always return True for this test
        from models import User
        mp.setattr(User, "verify_password", lambda self, pwd: True)
        
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login', json=data)
        
        assert response.status_code == 200
        assert 'access_token' in response.json

def test_login_invalid_credentials(client, mock_db):
    """Test login with invalid credentials"""
    mock_db['users'].find_one.return_value = None
    
    data = {
        'email': 'wrong@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/auth/login', json=data)
    
    assert response.status_code == 401

def test_get_current_user(client, mock_db, auth_header):
    """Test getting current user profile"""
    user_id = auth_header['user_id']
    mock_user = {
        '_id': ObjectId(user_id),
        'username': 'testuser',
        'email': 'test@example.com'
    }
    mock_db['users'].find_one.return_value = mock_user
    
    response = client.get('/api/auth/me', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 200
    assert response.json['user']['email'] == 'test@example.com'

def test_get_current_user_not_found(client, mock_db, auth_header):
    """Test getting current user when user deleted"""
    mock_db['users'].find_one.return_value = None
    
    response = client.get('/api/auth/me', headers={'Authorization': auth_header['Authorization']})
    
    assert response.status_code == 404

def test_refresh_token(client, mock_db):
    """Test token refresh"""
    # Create a refresh token
    from flask_jwt_extended import create_refresh_token
    
    with client.application.app_context():
        refresh_token = create_refresh_token(identity='507f1f77bcf86cd799439011')
        
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = client.post('/api/auth/refresh', headers=headers)
    
    assert response.status_code == 200
    assert 'access_token' in response.json
