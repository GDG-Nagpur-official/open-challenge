from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import Config
from app.database import init_indexes

from app.routes.apis import apis_bp
from app.routes.auth import auth_bp
from app.routes.logs import logs_bp
from app.routes.api_keys import api_keys_bp
from app.routes.execute import execute_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "http://localhost:3000",
                "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        },
        supports_credentials=True,
    )

    JWTManager(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(apis_bp)
    app.register_blueprint(api_keys_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(execute_bp)
   
    init_indexes()

    @app.route("/")
    def index():
        return jsonify({
            "message": "API Management System",
            "version": "1.0.0"
        })

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=(Config.FLASK_ENV == "development")
    )