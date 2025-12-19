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
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    CACHE_DEFAULT_TTL = int(os.getenv('CACHE_DEFAULT_TTL', 300))
    CACHE_APIS_TTL = int(os.getenv('CACHE_APIS_TTL', 300))
    CACHE_STATS_TTL = int(os.getenv('CACHE_STATS_TTL', 60))
    CACHE_PROFILE_TTL = int(os.getenv('CACHE_PROFILE_TTL', 600))
