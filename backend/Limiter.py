from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def rate_limit_key():
    """
    • Authenticated users → user_id
    • Unauthenticated users → IP address
    """
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            return f"user:{identity}"
    except Exception:
        pass

    return get_remote_address()

limiter = Limiter(
    key_func=rate_limit_key,
    default_limits=[]
)
