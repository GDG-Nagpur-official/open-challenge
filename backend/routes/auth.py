from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from database import users_collection
from models import User


from utils.util import serialize_doc, hash_password
import secrets

from utils.email_service import send_reset_email

from bson import ObjectId
from datetime import datetime, timedelta
import validators
import secrets


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ---------------- REGISTER ----------------
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


# ---------------- LOGIN ----------------
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


# ---------------- FORGOT PASSWORD ----------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email required"}), 400

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"message": "If email exists, reset link sent"}), 200

    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "reset_token": token,
            "reset_token_expiry": expiry
        }}
    )

    reset_link = f"http://localhost:3000/reset-password/{token}"

    print("TOKEN STORED IN DB:", token)
    send_reset_email(user["email"], reset_link)

    return jsonify({"message": "Reset link sent"}), 200


# ---------------- RESET PASSWORD ----------------
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    print("TOKEN RECEIVED FROM FRONTEND:", token)

    user = users_collection.find_one({"reset_token": token})

    print("USER FOUND:", user)

    if not user:
        return jsonify({"message": "Invalid or expired reset link"}), 400

    users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {"password": hash_password(new_password)},
            "$unset": {"reset_token": "", "reset_token_expiry": ""}
        }
    )

    return jsonify({"message": "Password updated successfully"}), 200

# ---------------- REFRESH TOKEN ----------------
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    
    return jsonify({
        'access_token': access_token
    }), 200


# ---------------- CURRENT USER ----------------
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
