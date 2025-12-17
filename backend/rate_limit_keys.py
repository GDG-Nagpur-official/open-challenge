from flask_jwt_extended import get_jwt_identity
from flask import request

def user_rate_limit_key():
    """
    Use user ID from JWT if authenticated,
    otherwise fall back to IP address
    """
    try:
        identity = get_jwt_identity()
        if identity:
            return f"user:{identity}"
    except Exception:
        pass

    # fallback for unauthenticated users
    return request.remote_addr
