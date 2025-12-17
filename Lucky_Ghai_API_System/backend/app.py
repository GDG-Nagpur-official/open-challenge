import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import init_indexes

from routes.auth import auth_bp
from routes.apis import apis_bp
from routes.api_keys import api_keys_bp
from routes.logs import logs_bp
from routes.execute import execute_bp

app = Flask(__name__)
app.config.from_object(Config)
logging.basicConfig(level=logging.INFO)

CORS(app)
jwt = JWTManager(app)
app.register_blueprint(auth_bp)
app.register_blueprint(apis_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(execute_bp)

@app.before_request
def log_request_info():

    app.logger.info(f"📝 Request: {request.method} {request.url}")
    if request.is_json:
        app.logger.info(f"📦 Body: {request.json}")


    try:
        init_indexes()
    except Exception as e:
        app.logger.warning(f"⚠️ Index init warning: {e}")

@app.after_request
def log_response_info(response):
    app.logger.info(f"✅ Response Status: {response.status_code}")
    return response

@app.route('/api/developer', methods=['GET'])
def developer_info():
    return jsonify({
        "developer": "Lucky Ghai",
        "event": "GDG DevFest 2025",
        "project": "API Management System",
        "status": "Ready for Buildathon"
    }), 200


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
            'execute': '/api/execute',
            'developer': '/api/developer'
        }
    }), 200

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=(Config.FLASK_ENV == 'development'))