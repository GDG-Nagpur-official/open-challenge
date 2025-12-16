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

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import get_jwt_identity

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)

def rate_limit_key():
    identity = get_jwt_identity()
    return identity if identity else get_remote_address()

limiter = Limiter(
    key_func=rate_limit_key,
    app=app,
    headers_enabled=True  
)


app.register_blueprint(auth_bp)
app.register_blueprint(apis_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(execute_bp)

@app.before_request
def initialize_db():
    init_indexes()

@app.route('/')
@limiter.limit("10 per minute", key_func=get_remote_address)
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
@limiter.limit("30 per minute", key_func=get_remote_address)
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