from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from database import users_collection
from models import User
from utils import serialize_doc
from bson import ObjectId
from datetime import datetime
import validators
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    if not validators.email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    if users_collection.find_one({'$or': [{'email': email}, {'username': username}]}):
        return jsonify({'error': 'User with this email or username already exists'}), 409
    
    user_data = User.create(username, email, password)
    result = users_collection.insert_one(user_data)
    
    user_data['_id'] = result.inserted_id
    
    access_token = create_access_token(identity=str(result.inserted_id))
    refresh_token = create_refresh_token(identity=str(result.inserted_id))
    
    return jsonify({
        'message': 'User registered successfully',
        'user': serialize_doc(user_data),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = users_collection.find_one({'email': email})
    
    if not user or not User.verify_password(user['password'], password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=str(user['_id']))
    refresh_token = create_refresh_token(identity=str(user['_id']))
    
    return jsonify({
        'message': 'Login successful',
        'user': serialize_doc(user),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    
    return jsonify({
        'access_token': access_token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': serialize_doc(user)
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    update_fields = {}
    
    # Update username if provided
    if 'username' in data and data['username']:
        username = data['username'].strip()
        # Check if username is taken by another user
        existing = users_collection.find_one({
            'username': username,
            '_id': {'$ne': ObjectId(user_id)}
        })
        if existing:
            return jsonify({'error': 'Username already taken'}), 409
        update_fields['username'] = username
    
    # Update email if provided
    if 'email' in data and data['email']:
        email = data['email'].strip()
        if not validators.email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        # Check if email is taken by another user
        existing = users_collection.find_one({
            'email': email,
            '_id': {'$ne': ObjectId(user_id)}
        })
        if existing:
            return jsonify({'error': 'Email already taken'}), 409
        update_fields['email'] = email
    
    # Update password if provided
    if 'password' in data and data['password']:
        password = data['password']
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        update_fields['password'] = hashed_password.decode('utf-8')
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_fields['updated_at'] = datetime.utcnow()
    
    users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': update_fields}
    )
    
    updated_user = users_collection.find_one({'_id': ObjectId(user_id)})
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': serialize_doc(updated_user)
    }), 200

@auth_bp.route('/profile/password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not all([current_password, new_password]):
        return jsonify({'error': 'Current password and new password are required'}), 400
    
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Verify current password
    if not User.verify_password(user['password'], current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    if len(new_password) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {
            'password': hashed_password.decode('utf-8'),
            'updated_at': datetime.utcnow()
        }}
    )
    
    return jsonify({
        'message': 'Password changed successfully'
    }), 200
