from datetime import datetime, timedelta
import hashlib
import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from bson import ObjectId
import validators
from app.database import users_collection
from app.models.models import User
from app.utils import send_reset_email
from app.utils.utils import generate_reset_token, serialize_doc

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ================= REGISTER =================
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


# ================= LOGIN =================
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

    return jsonify({
        'message': 'Login successful',
        'user': serialize_doc(user),
        'access_token': create_access_token(identity=str(user['_id'])),
        'refresh_token': create_refresh_token(identity=str(user['_id']))
    }), 200


# ================= REFRESH TOKEN =================
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return jsonify({
        'access_token': create_access_token(identity=identity)
    }), 200


# ================= CURRENT USER =================
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user': serialize_doc(user)}), 200


# Note: forgot-password and reset-password routes moved to their own modules
# to keep handlers and dependencies consistent (see forgot_password.py and reset_password.py).
