# AI Coding Guidelines for API Management Backend

## Architecture Overview
This Flask-based API management system enables users to create, manage, and execute external APIs through a secure proxy with authentication and comprehensive logging.

**Core Components:**
- `app.py`: Main Flask application with CORS, JWT authentication, and route blueprints
- `database.py`: MongoDB connection and collection definitions with optimized indexes
- `models.py`: Data model classes with static factory methods for document creation
- `utils.py`: Utility functions for serialization, API key generation, and authentication decorators
- `routes/`: Modular blueprints for auth, API management, key management, logging, and execution

**Data Flow:**
1. Users register/login via JWT-authenticated endpoints in `routes/auth.py`
2. Authenticated users create API definitions in `routes/apis.py`
3. Users generate API keys in `routes/api_keys.py` for execution access
4. External requests execute APIs via `routes/execute.py` proxy with API key authentication
5. All executions logged in `routes/logs.py` for monitoring

## Key Patterns & Conventions
- **Serialization**: Always use `serialize_doc()`/`serialize_docs()` from `utils.py` to convert ObjectId fields to strings and exclude sensitive data like passwords
- **Authentication**: JWT tokens for user management endpoints, X-API-Key headers for API execution
- **Password Security**: Hash passwords with bcrypt in `User.create()` method
- **API Execution**: Proxy requests using Python `requests` library with 30s timeout, full request/response logging
- **Error Handling**: Return JSON responses with 'error' key for client errors
- **Database**: Use ObjectId for document references, maintain unique indexes on email/username/api_key
- **Timestamps**: Store all timestamps as UTC datetime objects

## Development Workflow
- **Local Development**: Run `python app.py` (enables debug mode when `FLASK_ENV=development`)
- **Production**: Use Docker container with gunicorn (4 workers) as defined in `Dockerfile`
- **Environment**: Configure via `.env` file loaded in `config.py` (MongoDB URI, JWT secrets, etc.)
- **Database**: Requires MongoDB instance; defaults to localhost:27017

## Code Examples
**Creating a new API document:**
```python
api_data = API.create(user_id, name, description, endpoint, method, headers, params)
apis_collection.insert_one(api_data)
```

**Serializing for response:**
```python
return jsonify({'api': serialize_doc(api_doc)}), 200
```

**API key authentication:**
```python
@execute_bp.route('/<api_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@api_key_required
def execute_api(api_id):
    # Access authenticated user via request.user_id
```