from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from database import init_indexes

from routes.auth import auth_bp
from routes.apis import apis_bp
from routes.api_keys import api_keys_bp
from routes.logs import logs_bp
from routes.execute import execute_bp


def user_or_ip_key():
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            return f"user:{identity}"
    except Exception:
        pass
    return f"ip:{get_remote_address()}"


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri=Config.RATE_LIMIT_REDIS_URI,
    default_limits=["200 per hour"],
    headers_enabled=True,
)

user_limited = limiter.shared_limit(
    "100 per hour",
    scope="user_rate_limit",
    key_func=user_or_ip_key,
)

app.register_blueprint(auth_bp)
app.register_blueprint(apis_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(execute_bp)

limiter.limit("50 per hour", override_defaults=False)(auth_bp)
limiter.limit("150 per hour", override_defaults=False)(apis_bp)
limiter.limit("200 per hour", override_defaults=False)(api_keys_bp)
limiter.limit("200 per hour", override_defaults=False)(logs_bp)
limiter.limit("100 per hour", override_defaults=False)(execute_bp)


@app.before_request
def initialize_db():
    init_indexes()


@app.route("/")
def index():
    return jsonify(
        {
            "message": "API Management System",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/api/auth",
                "apis": "/api/apis",
                "api_keys": "/api/keys",
                "logs": "/api/logs",
                "execute": "/api/execute",
            },
        }
    ), 200


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    return (
        jsonify(
            {
                "error": "Too many requests",
                "message": "Rate limit exceeded. Please try again later.",
            }
        ),
        429,
        {"Retry-After": str(e.reset_in)},
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=(Config.FLASK_ENV == "development"),
    )
