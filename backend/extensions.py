from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import get_jwt_identity

def rate_limit_key():
    
    identity = get_jwt_identity()
    return identity if identity else get_remote_address()

limiter = Limiter(
    key_func=rate_limit_key,
    headers_enabled=True  
)