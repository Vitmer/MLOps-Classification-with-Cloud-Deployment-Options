import io
from fastapi.testclient import TestClient
from PIL import Image
import unittest
import logging
from src.api.main import app

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class TestMainApp(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        logging.info("Setting up TestClient and adding a test user.")
        # Ensure registration route is available or mock it
        self.client.post("/register", json={
            "username": "test_user",
            "password": "test_password"
        })

    def test_login(self):
        logging.info("Testing login route.")
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }
        response = self.client.post("/login", data=login_data)
        logging.debug(f"Response JSON: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_upload_image(self):
        logging.info("Testing image upload route.")
        # Create a test image in memory
        image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Mock the /upload_image route response
        response = self.client.post("/upload_image", files={"file": ("test_image.jpg", img_byte_arr, "image/jpeg")})
        self.assertEqual(response.status_code, 200)

    def test_retrain_model(self):
        logging.info("Testing retrain model route.")
        # Mock the /retrain route response
        response = self.client.post("/retrain", json={"retrain_data": "some_data"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()