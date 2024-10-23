import unittest
from unittest.mock import patch, MagicMock
import logging
import numpy as np
from src.api.util_model import predict_classification, train_model_on_new_data, evaluate_model_on_untrained_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class TestUtilModel(unittest.TestCase):

    @patch('src.api.util_model.predict_classification')
    def test_predict_classification(self, mock_predict):
        logging.info("Testing predict_classification function.")
        # Create a mock vectorizer
        mock_vectorizer = MagicMock()
        mock_vectorizer.transform.return_value.toarray.return_value = [[0.1, 0.2, 0.3]]

        # Mock image object with correct shape
        mock_image = MagicMock()
        mock_image.size = (224, 224)  # Correct image size

        # Pass the mock vectorizer and image
        result = predict_classification("input_data", mock_vectorizer, "designation", "description", mock_image)
        self.assertEqual(result, "class_a")
        mock_predict.assert_called_once_with("input_data", mock_vectorizer, "designation", "description", mock_image)
        logging.debug("Classification prediction test passed.")

    @patch('src.api.util_model.train_model_on_new_data')
    def test_train_model_on_new_data(self, mock_train):
        logging.info("Testing train_model_on_new_data function.")

        # Create a mock session
        mock_session = MagicMock()
        mock_train.return_value = {"accuracy": 0.95}

        # Ensure X_train and Y_train are not empty
        X_train = np.array([[0.1, 0.2, 0.3]])
        Y_train = np.array([1])

        # Pass the mock session and valid arrays
        result = train_model_on_new_data(X_train, Y_train, mock_session)
        self.assertEqual(result["accuracy"], 0.95)
        mock_train.assert_called_once_with(X_train, Y_train, mock_session)
        logging.debug("Model training test passed.")

    @patch('src.api.util_model.evaluate_model_on_untrained_data')
    def test_evaluate_model_on_untrained_data(self, mock_evaluate):
        logging.info("Testing evaluate_model_on_untrained_data function.")

        # Create a mock session and model
        mock_session = MagicMock()
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([[0.8, 0.2], [0.4, 0.6]])

        # Mock valid data for X_test and X_image
        X_text = np.array([[0.1, 0.2, 0.3]])
        X_image = np.random.rand(1, 224, 224, 3).astype(np.float32)  # Create a valid image tensor

        # Pass the mock model and session
        result = evaluate_model_on_untrained_data(X_text, X_image, mock_session)
        self.assertEqual(result["f1_score"], 0.87)
        mock_evaluate.assert_called_once_with(X_text, X_image, mock_session)
        logging.debug("Model evaluation test passed.")

if __name__ == '__main__':
    unittest.main()