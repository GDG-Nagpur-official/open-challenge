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
    MONGODB_SERVER_SELECTION_TIMEOUT_MS = int(os.getenv('MONGODB_SERVER_SELECTION_TIMEOUT_MS', 3000))
    MONGODB_MAX_RETRIES = int(os.getenv('MONGODB_MAX_RETRIES', 5))
    MONGODB_BACKOFF_BASE = float(os.getenv('MONGODB_BACKOFF_BASE', 0.5))
    MONGODB_BACKOFF_MAX = float(os.getenv('MONGODB_BACKOFF_MAX', 8))
    PORT = int(os.getenv('PORT', 5000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
