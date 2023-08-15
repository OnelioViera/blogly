import unittest
from app import app  # Import your Flask app instance

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_redirect(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "http://localhost/users")

    def test_show_users(self):
        response = self.app.get("/users")
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your application's behavior

    def test_new_user(self):
        response = self.app.get("/users/new")
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your application's behavior
        
    def test_add_user_form_submission(self):
        data = {"first_name": "New", "last_name": "User", "image_url": "https://example.com/image.jpg"}
        response = self.app.post("/users/new", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your application's behavior after form submission

    # Add more test methods for other routes

if __name__ == "__main__":
    unittest.main()
