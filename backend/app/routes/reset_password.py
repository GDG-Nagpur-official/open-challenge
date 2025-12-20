from datetime import datetime
import hashlib
from flask import request, jsonify
from flask_bcrypt import Bcrypt

from app.database import users_collection
from app.routes.auth import auth_bp  
bcrypt = Bcrypt()


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()

    token = data.get("token")
    new_password = data.get("password")

    if not token or not new_password:
        return jsonify({"error": "Token and password are required"}), 400

    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    user = users_collection.find_one({
        "reset_token": hashed_token,
        "reset_token_expiry": {"$gt": datetime.utcnow()}
    })

    if not user:
        return jsonify({"error": "Invalid or expired token"}), 400

    hashed_pw = bcrypt.generate_password_hash(new_password).decode("utf-8")

    users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {"password": hashed_pw},
            "$unset": {"reset_token": "", "reset_token_expiry": ""}
        }
    )

    return jsonify({"message": "Password reset successful"}), 200
