import os
import sys
from datetime import datetime, timedelta
from bson import ObjectId
from database import users_collection, apis_collection
from models import User, API

# Add current directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def seed_database():
    print("Seeding database...")

    # 1. Create a test user
    test_email = "test@example.com"
    user = users_collection.find_one({'email': test_email})
    
    if not user:
        print(f"Creating user {test_email}...")
        user_data = User.create("testuser", test_email, "password123")
        result = users_collection.insert_one(user_data)
        user_id = result.inserted_id
    else:
        print(f"User {test_email} already exists.")
        user_id = user['_id']

    # 2. Create sample APIs
    # Clear existing APIs for this user to avoid duplicates if run multiple times
    # apis_collection.delete_many({'user_id': user_id}) 
    # Commented out delete to just add more records as requested

    sample_apis = [
        {
            "name": "User Service",
            "description": "API for user management",
            "endpoint": "https://api.example.com/users",
            "method": "GET",
            "status": "active",
            "created_offset": 0
        },
        {
            "name": "Payment Gateway",
            "description": "Process payments",
            "endpoint": "https://api.payment.com/charge",
            "method": "POST",
            "status": "active",
            "created_offset": 1
        },
        {
            "name": "Analytics Data",
            "description": "Get analytics reports",
            "endpoint": "https://api.analytics.io/reports",
            "method": "GET",
            "status": "inactive",
            "created_offset": 2
        },
        {
            "name": "Update Profile",
            "description": "Update user profile",
            "endpoint": "https://api.example.com/users/profile",
            "method": "PUT",
            "status": "active",
            "created_offset": 3
        },
        {
            "name": "Delete Account",
            "description": "Remove user account",
            "endpoint": "https://api.example.com/users/account",
            "method": "DELETE",
            "status": "inactive",
            "created_offset": 4
        },
        {
            "name": "Weather Info",
            "description": "Get current weather",
            "endpoint": "https://api.weather.com/current",
            "method": "GET",
            "status": "active",
            "created_offset": 5
        },
        {
            "name": "Inventory Check",
            "description": "Check product stock",
            "endpoint": "https://api.store.com/inventory",
            "method": "GET",
            "status": "active",
            "created_offset": 6
        },
        {
            "name": "Order Submit",
            "description": "Submit a new order",
            "endpoint": "https://api.store.com/orders",
            "method": "POST",
            "status": "active",
            "created_offset": 7
        },
        {
            "name": "Legacy System",
            "description": "Old legacy API",
            "endpoint": "https://legacy.system.com/api",
            "method": "GET",
            "status": "inactive",
            "created_offset": 8
        },
        {
            "name": "Notification Service",
            "description": "Send push notifications",
            "endpoint": "https://api.notify.me/send",
            "method": "POST",
            "status": "active",
            "created_offset": 9
        }
    ]

    print(f"Adding {len(sample_apis)} APIs...")
    
    for api in sample_apis:
        # Create API object
        api_data = API.create(
            user_id, 
            api['name'], 
            api['description'], 
            api['endpoint'], 
            api['method']
        )
        # Override status and dates for testing sorting/filtering
        api_data['status'] = api['status']
        # Spread creation dates over the last 10 days
        api_data['created_at'] = datetime.utcnow() - timedelta(days=api['created_offset'])
        api_data['updated_at'] = api_data['created_at']
        
        apis_collection.insert_one(api_data)

    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
