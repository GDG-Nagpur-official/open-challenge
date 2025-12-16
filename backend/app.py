from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import init_indexes
from flasgger import Swagger


from routes.auth import auth_bp
from routes.apis import apis_bp
from routes.api_keys import api_keys_bp
from routes.logs import logs_bp
from routes.execute import execute_bp

app = Flask(__name__)
swagger_config = {
    "openapi": "3.0.2",
    "title": "Open Challenge API",
    "version": "1.0.0",
    "description": "Interactive API documentation for Open Challenge backend",
    "specs_route": "/api/docs"
}

swagger_template = {
    "openapi": "3.0.2",
    "info": {
        "title": "Open Challenge API",
        "description": "Interactive API documentation for Open Challenge backend",
        "version": "1.0.0"
    },
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)

# app.register_blueprint(auth_bp)
# app.register_blueprint(apis_bp)
# app.register_blueprint(api_keys_bp)
# app.register_blueprint(logs_bp)
# app.register_blueprint(execute_bp)

# @app.before_request
# def initialize_db():
 #   init_indexes()

@app.route('/')
def index():
    return jsonify({
        'message': 'API Management System',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'apis': '/api/apis',
            'api_keys': '/api/keys',
            'logs': '/api/logs',
            'execute': '/api/execute'
        }
    }), 200

@app.route('/health')
def health():
    """
    Health Check API
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is healthy
        content:
          application/json:
            example:
              status: healthy
    """
    return jsonify({'status': 'healthy'}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=(Config.FLASK_ENV == 'development'))
