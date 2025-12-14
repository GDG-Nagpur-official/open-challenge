# API Management System

A comprehensive full-stack application for managing, monitoring, and analyzing APIs. Built with Flask (Python) backend and React frontend, featuring JWT authentication, MongoDB database, and Docker support.

## Features

### Core Functionality
- **API Management**: Create, read, update, and delete API endpoints
- **Authentication**: JWT-based authentication with secure user registration and login
- **API Key Management**: Generate and manage API keys for secure API access
- **Request Logging**: Automatic logging of all API requests with detailed metrics
- **Analytics Dashboard**: Real-time statistics and request history visualization
- **Rate Limiting Ready**: Infrastructure for implementing rate limiting
- **Docker Support**: Fully containerized with Docker Compose

### Technical Features
- RESTful API architecture
- MongoDB for flexible data storage
- React with Hooks and Context API
- Responsive UI design
- Token refresh mechanism
- CORS enabled
- Production-ready with Gunicorn and Nginx

## Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: MongoDB 7.0
- **Authentication**: Flask-JWT-Extended
- **Password Hashing**: bcrypt
- **Server**: Gunicorn

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Notifications**: React Toastify
- **Icons**: Lucide React
- **Build Tool**: Create React App

### DevOps
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **Database**: MongoDB in Docker

## Project Structure

```
api-management-system/
├── backend/
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── apis.py          # API CRUD operations
│   │   ├── api_keys.py      # API key management
│   │   ├── logs.py          # Request logs and stats
│   │   └── execute.py       # API execution proxy
│   ├── app.py               # Main Flask application
│   ├── config.py            # Configuration settings
│   ├── database.py          # MongoDB connection
│   ├── models.py            # Data models
│   ├── utils.py             # Helper functions
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # Auth context
│   │   ├── utils/           # API utilities
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   ├── public/              # Static files
│   ├── package.json         # Node dependencies
│   ├── Dockerfile           # Frontend container
│   └── nginx.conf           # Nginx configuration
├── docker-compose.yml       # Docker orchestration
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # Contribution guidelines
└── README.md               # This file
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB 7.0+
- Docker & Docker Compose (optional)

### Installation

#### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/api-management-system.git
cd api-management-system
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

#### Option 2: Manual Setup

**Backend Setup:**

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Start MongoDB (ensure it's running on localhost:27017)

6. Run the application:
```bash
python app.py
```

**Frontend Setup:**

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API URL
```

4. Start development server:
```bash
npm start
```

5. Access at http://localhost:3000

## API Documentation

### Authentication Endpoints

**Register User**
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "string",
  "password": "string"
}
```

**Get Current User**
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### API Management Endpoints

**List APIs**
```http
GET /api/apis?page=1&limit=10
Authorization: Bearer <token>
```

**Create API**
```http
POST /api/apis
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "endpoint": "string",
  "method": "GET|POST|PUT|DELETE|PATCH",
  "headers": {},
  "params": {}
}
```

**Update API**
```http
PUT /api/apis/<api_id>
Authorization: Bearer <token>
Content-Type: application/json
```

**Delete API**
```http
DELETE /api/apis/<api_id>
Authorization: Bearer <token>
```

### API Key Endpoints

**List API Keys**
```http
GET /api/keys
Authorization: Bearer <token>
```

**Create API Key**
```http
POST /api/keys
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "string"
}
```

**Delete API Key**
```http
DELETE /api/keys/<key_id>
Authorization: Bearer <token>
```

**Toggle API Key**
```http
PATCH /api/keys/<key_id>/toggle
Authorization: Bearer <token>
```

### Logs & Analytics Endpoints

**Get Logs**
```http
GET /api/logs?page=1&limit=20&api_id=<optional>
Authorization: Bearer <token>
```

**Get Statistics**
```http
GET /api/logs/stats
Authorization: Bearer <token>
```

### Execute API Endpoint

**Execute API**
```http
GET|POST|PUT|DELETE|PATCH /api/execute/<api_id>
X-API-Key: <your-api-key>
```

## Usage Examples

### Creating an API

1. Register/Login to the application
2. Navigate to Dashboard
3. Click "Create API"
4. Fill in API details:
   - Name: "JSONPlaceholder Posts"
   - Endpoint: "https://jsonplaceholder.typicode.com/posts"
   - Method: "GET"
5. Save the API

### Generating an API Key

1. Navigate to "API Keys"
2. Click "Create API Key"
3. Enter a name for the key
4. Copy the generated key
5. Use it in your requests with `X-API-Key` header

### Viewing Analytics

1. Navigate to "Analytics"
2. View real-time statistics:
   - Total requests
   - Success/error rates
   - Average response time
3. Browse request history with pagination

## Environment Variables

### Backend (.env)
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MONGODB_URI=mongodb://localhost:27017/api_management
PORT=5000
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

- Passwords are hashed using bcrypt
- JWT tokens for secure authentication
- API keys for service-to-service authentication
- CORS configured for security
- Environment variables for sensitive data

## Roadmap

- [ ] Rate limiting implementation
- [ ] Webhook support
- [ ] API versioning
- [ ] Advanced filtering and search
- [ ] Export analytics to CSV/PDF
- [ ] Email notifications
- [ ] Team collaboration features
- [ ] API documentation generator
- [ ] GraphQL support
- [ ] WebSocket support for real-time updates

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- Flask community for excellent documentation
- React team for the amazing framework
- MongoDB for the flexible database solution
- All open-source contributors

---

**Built with ❤️ using Flask and React**
