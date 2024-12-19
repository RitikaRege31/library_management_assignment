import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"

class TestBooksAPI(unittest.TestCase):
    def test_add_book(self):
        data = {"title": "Test Book", "author": "Test Author", "published_year": 2023}
        response = requests.post(f"{BASE_URL}/books", json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        response = requests.get(f"{BASE_URL}/books")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
