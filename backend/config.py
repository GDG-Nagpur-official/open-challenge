import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/api_management')
    PORT = int(os.getenv('PORT', 5000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Rate Limiting Configuration
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_GLOBAL = os.getenv('RATELIMIT_GLOBAL', '10000 per hour')
    RATELIMIT_EXECUTE_API = os.getenv('RATELIMIT_EXECUTE_API', '100 per hour')
    RATELIMIT_AUTH = os.getenv('RATELIMIT_AUTH', '20 per hour')
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '500 per hour')
