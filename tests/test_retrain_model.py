import unittest
from unittest.mock import patch, MagicMock
import gc
import logging
from src.api.retrain_model import build_model, free_memory
import tensorflow as tf

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class TestRetrainModel(unittest.TestCase):

    @patch('src.api.retrain_model.gc.collect')
    @patch('src.api.retrain_model.logging.debug')
    def test_free_memory(self, mock_logging_debug, mock_gc_collect):
        logging.info("Testing free_memory function.")
        free_memory()
        mock_gc_collect.assert_called_once()
        mock_logging_debug.assert_called_once_with("Memory freed using garbage collector.")
        logging.debug("free_memory test passed.")

    @patch('tensorflow.keras.models.Model.compile')
    def test_build_model(self, mock_compile):
        logging.info("Testing build_model function.")
        input_shape_text = 100
        input_shape_image = 64
        num_classes = 27
        
        # Build the model
        model = build_model(input_shape_text, input_shape_image, num_classes)
        
        # Check that compile was called with the correct arguments
        mock_compile.assert_called_once()
        compile_call_args = mock_compile.call_args[1]  # Retrieve keyword arguments
        self.assertIsInstance(compile_call_args['optimizer'], tf.keras.optimizers.Nadam)
        self.assertEqual(compile_call_args['loss'], 'sparse_categorical_crossentropy')
        self.assertEqual(compile_call_args['metrics'], ['accuracy'])
        logging.debug("Model compiled with expected parameters.")

if __name__ == '__main__':
    unittest.main()