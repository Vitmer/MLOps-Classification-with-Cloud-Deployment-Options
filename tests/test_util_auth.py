import unittest
from unittest.mock import patch
import logging
from src.api.util_auth import get_password_hash, verify_password, create_access_token, verify_access_token

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class TestUtilAuth(unittest.TestCase):

    @patch('src.api.util_auth.pwd_context.hash')
    def test_get_password_hash(self, mock_hash):
        logging.info("Testing get_password_hash function.")
        mock_hash.return_value = "hashed_password"
        result = get_password_hash("my_password")
        self.assertEqual(result, "hashed_password")
        mock_hash.assert_called_once_with("my_password")
        logging.debug("Password hashing test passed.")

    @patch('src.api.util_auth.pwd_context.verify')
    def test_verify_password(self, mock_verify):
        logging.info("Testing verify_password function.")
        mock_verify.return_value = True
        result = verify_password("my_password", "hashed_password")
        self.assertTrue(result)
        mock_verify.assert_called_once_with("my_password", "hashed_password")
        logging.debug("Password verification test passed.")

    @patch('src.api.util_auth.jwt.encode')
    def test_create_access_token(self, mock_jwt_encode):
        logging.info("Testing create_access_token function.")
        mock_jwt_encode.return_value = "jwt_token"
        data = {"sub": "username"}
        result = create_access_token(data)
        self.assertEqual(result, "jwt_token")
        mock_jwt_encode.assert_called_once_with(data, "your_secret_key", algorithm="HS256")
        logging.debug("Access token creation test passed.")

    @patch('src.api.util_auth.jwt.decode')
    def test_verify_access_token(self, mock_jwt_decode):
        logging.info("Testing verify_access_token function.")
        mock_jwt_decode.return_value = {"sub": "username"}
        result = verify_access_token("jwt_token")
        self.assertEqual(result, {"username": "username"})
        mock_jwt_decode.assert_called_once_with("jwt_token", "your_secret_key", algorithms=["HS256"])
        logging.debug("Access token verification test passed.")

if __name__ == '__main__':
    unittest.main()