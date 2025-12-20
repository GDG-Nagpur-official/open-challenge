import os
from datetime import datetime, timedelta
from flask import request, jsonify

from app.database import users_collection
from app.routes.auth import auth_bp
from app.utils import send_reset_email
from app.utils.utils import generate_reset_token


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = users_collection.find_one({"email": email})

    # Security: same response even if email doesn't exist
    if not user:
        return jsonify({"message": "If email exists, reset link sent"}), 200

    raw_token, hashed_token = generate_reset_token()

    users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "reset_token": hashed_token,
                "reset_token_expiry": datetime.utcnow() + timedelta(hours=1)
            }
        }
    )

    reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password?token={raw_token}"
    send_reset_email(email, reset_url)

    return jsonify({"message": "Reset email sent"}), 200
