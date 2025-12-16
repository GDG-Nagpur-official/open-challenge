import unittest
import json
import sys
import os
from app import app
from database import users_collection, apis_collection

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestDashboardAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Login to get token
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.app.post('/api/auth/login', 
                               data=json.dumps(login_data),
                               content_type='application/json')
        self.token = json.loads(response.data)['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def test_1_search(self):
        print("\nTesting Search...")
        # Search for "Payment"
        response = self.app.get('/api/apis/?search=Payment', headers=self.headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.data)
        data = json.loads(response.data)
        apis = data['apis']
        print(f"Search 'Payment' found {len(apis)} APIs")
        self.assertTrue(len(apis) > 0)
        self.assertTrue(any('Payment' in api['name'] for api in apis))

    def test_2_filter_method(self):
        print("\nTesting Filter by Method...")
        # Filter by POST
        response = self.app.get('/api/apis/?method=POST', headers=self.headers)
        data = json.loads(response.data)
        apis = data['apis']
        print(f"Filter 'POST' found {len(apis)} APIs")
        self.assertTrue(len(apis) > 0)
        for api in apis:
            self.assertEqual(api['method'], 'POST')

    def test_3_filter_status(self):
        print("\nTesting Filter by Status...")
        # Filter by inactive
        response = self.app.get('/api/apis/?status=inactive', headers=self.headers)
        data = json.loads(response.data)
        apis = data['apis']
        print(f"Filter 'inactive' found {len(apis)} APIs")
        self.assertTrue(len(apis) > 0)
        for api in apis:
            self.assertEqual(api['status'], 'inactive')

    def test_4_sort_created_desc(self):
        print("\nTesting Sort Created Desc...")
        response = self.app.get('/api/apis/?sort_by=created_at&sort_order=desc', headers=self.headers)
        data = json.loads(response.data)
        apis = data['apis']
        # Check if dates are in descending order
        from email.utils import parsedate_to_datetime
        dates = [parsedate_to_datetime(api['created_at']) for api in apis]
        self.assertEqual(dates, sorted(dates, reverse=True))
        print("Sort Desc verified")

    def test_5_sort_created_asc(self):
        print("\nTesting Sort Created Asc...")
        response = self.app.get('/api/apis/?sort_by=created_at&sort_order=asc', headers=self.headers)
        data = json.loads(response.data)
        apis = data['apis']
        # Check if dates are in ascending order
        from email.utils import parsedate_to_datetime
        dates = [parsedate_to_datetime(api['created_at']) for api in apis]
        self.assertEqual(dates, sorted(dates))
        print("Sort Asc verified")

    def test_6_pagination(self):
        print("\nTesting Pagination...")
        limit = 3
        response = self.app.get(f'/api/apis/?page=1&limit={limit}', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(len(data['apis']), limit)
        self.assertEqual(data['page'], 1)
        print(f"Pagination Page 1 Limit {limit} verified")

        # Page 2
        response = self.app.get(f'/api/apis/?page=2&limit={limit}', headers=self.headers)
        data_p2 = json.loads(response.data)
        self.assertEqual(len(data_p2['apis']), limit)
        self.assertEqual(data_p2['page'], 2)
        
        # Ensure different data
        ids_p1 = [api['_id'] for api in data['apis']]
        ids_p2 = [api['_id'] for api in data_p2['apis']]
        self.assertTrue(set(ids_p1).isdisjoint(set(ids_p2)))
        print("Pagination Page 2 verified")

if __name__ == '__main__':
    unittest.main()
