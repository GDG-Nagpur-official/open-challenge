from flask import Flask, jsonify
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

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

CORS(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(apis_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(execute_bp)

@app.before_request
def initialize_db():
    init_indexes()

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
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=(Config.FLASK_ENV == 'development'))
