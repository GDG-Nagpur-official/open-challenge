from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource
from config import Config
from database import init_indexes

from routes.auth import auth_bp
from routes.apis import apis_bp
from routes.api_keys import api_keys_bp
from routes.logs import logs_bp
from routes.execute import execute_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)

# -----------------------------
# Swagger / OpenAPI Config
# -----------------------------
authorizations = {
    "BearerAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "JWT Authorization header. Example: Bearer <token>"
    }
}

api = Api(
    app,
    version="1.0.0",
    title="API Management System",
    description="Interactive Swagger/OpenAPI documentation for API Management System",
    authorizations=authorizations,
    security="BearerAuth",
    doc="/api/docs"   # Swagger UI endpoint
)

# -----------------------------
# Register Blueprints
# -----------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(apis_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(execute_bp)

# -----------------------------
# Swagger Base Routes
# -----------------------------
@api.route("/")
class Index(Resource):
    def get(self):
        """API Home"""
        return {
            "message": "API Management System",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/api/auth",
                "apis": "/api/apis",
                "api_keys": "/api/keys",
                "logs": "/api/logs",
                "execute": "/api/execute",
                "docs": "/api/docs",
                "openapi": "/api/openapi.json"
            }
        }, 200


@api.route("/health")
class Health(Resource):
    def get(self):
        """Health check"""
        return {"status": "healthy"}, 200


# -----------------------------
# OpenAPI JSON Endpoint
# -----------------------------
@app.route("/api/openapi.json")
def openapi_spec():
    return jsonify(api.__schema__)


# -----------------------------
# DB Initialization
# -----------------------------
with app.app_context():
    try:
        init_indexes()
    except Exception as e:
        app.logger.warning(f"MongoDB not connected: {e}")



# -----------------------------
# Error Handlers
# -----------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# -----------------------------
# App Runner
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=(Config.FLASK_ENV == "development")
    )
