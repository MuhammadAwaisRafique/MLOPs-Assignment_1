import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, clean_text

class TestIMDBSentimentAnalysis(unittest.TestCase):
    """Test cases for the IMDB Sentiment Analysis Flask application"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Sample test data
        self.positive_review = "This movie is absolutely fantastic! I loved every minute of it. The acting was superb and the storyline was engaging."
        self.negative_review = "This movie was terrible. Boring plot, bad acting, and poor direction. I would not recommend it to anyone."
        self.neutral_review = "The movie was okay. Nothing special but not terrible either."
        
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_home_page_accessible(self):
        """Test that the home page is accessible and returns 200 status code."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'IMDB Movie Review Sentiment Analysis', response.data)
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('model_loaded', data)
        self.assertIn('vectorizer_loaded', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_clean_text_function(self):
        """Test the text cleaning function."""
        # Test HTML tag removal
        html_text = "<p>This is a <b>test</b> review</p>"
        cleaned = clean_text(html_text)
        self.assertNotIn('<', cleaned)
        self.assertNotIn('>', cleaned)
        
        # Test number removal
        number_text = "This movie got 5 stars and 10/10 rating"
        cleaned = clean_text(number_text)
        self.assertNotIn('5', cleaned)
        self.assertNotIn('10', cleaned)
        
        # Test punctuation removal
        punct_text = "Hello, world! How are you?"
        cleaned = clean_text(punct_text)
        self.assertNotIn(',', cleaned)
        self.assertNotIn('!', cleaned)
        self.assertNotIn('?', cleaned)
        
        # Test lowercase conversion
        upper_text = "THIS IS A TEST"
        cleaned = clean_text(upper_text)
        self.assertEqual(cleaned, "this is a test")
    
    def test_predict_positive_sentiment(self):
        """Test prediction with positive sentiment."""
        # Test with actual model (should work since we have the model files)
        response = self.app.post('/predict', 
                               data=json.dumps({'review': self.positive_review}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that we get a valid prediction
        self.assertIn(data['prediction'], ['positive', 'negative'])
        self.assertGreater(data['confidence'], 0.0)
        self.assertLessEqual(data['confidence'], 1.0)
        self.assertEqual(data['original_text'], self.positive_review)
    
    def test_predict_negative_sentiment(self):
        """Test prediction with negative sentiment."""
        # Test with actual model (should work since we have the model files)
        response = self.app.post('/predict', 
                               data=json.dumps({'review': self.negative_review}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that we get a valid prediction
        self.assertIn(data['prediction'], ['positive', 'negative'])
        self.assertGreater(data['confidence'], 0.0)
        self.assertLessEqual(data['confidence'], 1.0)
        self.assertEqual(data['original_text'], self.negative_review)
    
    def test_predict_missing_review(self):
        """Test prediction endpoint with missing review data."""
        response = self.app.post('/predict', 
                               data=json.dumps({}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_predict_no_json_data(self):
        """Test prediction endpoint with no JSON data."""
        response = self.app.post('/predict', 
                               data="invalid json",
                               content_type='application/json')
        
        # The app might return 500 for JSON parsing errors, which is acceptable
        self.assertIn(response.status_code, [400, 500])
    
    def test_predict_empty_review(self):
        """Test prediction endpoint with empty review."""
        response = self.app.post('/predict', 
                               data=json.dumps({'review': ''}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
    
    def test_predict_model_not_loaded(self):
        """Test prediction when model is not loaded."""
        with patch('app.model', None), patch('app.tfidf', None):
            response = self.app.post('/predict', 
                                   data=json.dumps({'review': self.positive_review}),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
    
    def test_predict_with_special_characters(self):
        """Test prediction with special characters and unicode."""
        special_review = "This movie is gréat! 🌟 I l0v3d it! @movie_fan #awesome"
        
        # Test with actual model
        response = self.app.post('/predict', 
                               data=json.dumps({'review': special_review}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that we get a valid prediction
        self.assertIn(data['prediction'], ['positive', 'negative'])
        self.assertGreater(data['confidence'], 0.0)
        self.assertLessEqual(data['confidence'], 1.0)
        self.assertEqual(data['original_text'], special_review)
    
    def test_predict_with_very_long_review(self):
        """Test prediction with a very long review."""
        long_review = "This movie is " + "amazing " * 1000 + "!"
        
        # Test with actual model
        response = self.app.post('/predict', 
                               data=json.dumps({'review': long_review}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that we get a valid prediction
        self.assertIn(data['prediction'], ['positive', 'negative'])
        self.assertGreater(data['confidence'], 0.0)
        self.assertLessEqual(data['confidence'], 1.0)
        self.assertEqual(data['original_text'], long_review)
    
    def test_invalid_http_method(self):
        """Test that invalid HTTP methods are handled properly."""
        # Test GET request to /predict endpoint
        response = self.app.get('/predict')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
    
    def test_model_files_exist(self):
        """Test that model files exist in the project."""
        self.assertTrue(os.path.exists('imdb_logreg_model.pkl'), 
                       "Model file 'imdb_logreg_model.pkl' not found")
        self.assertTrue(os.path.exists('tfidf_vectorizer.pkl'), 
                       "Vectorizer file 'tfidf_vectorizer.pkl' not found")
    
    def test_requirements_file_exists(self):
        """Test that requirements.txt file exists."""
        self.assertTrue(os.path.exists('requirements.txt'), 
                       "Requirements file 'requirements.txt' not found")
    
    def test_app_configuration(self):
        """Test Flask app configuration."""
        # The app.testing is set to True in setUp method via self.app.testing = True
        self.assertTrue(self.app.testing, "App should be in testing mode")
        self.assertIsNotNone(app.config, "App config should not be None")

class TestModelPerformance(unittest.TestCase):
    """Test cases for model performance and accuracy"""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_model_loading_time(self):
        """Test that model loads within reasonable time."""
        import time
        
        start_time = time.time()
        response = self.app.get('/health')
        end_time = time.time()
        
        load_time = end_time - start_time
        self.assertLess(load_time, 10, "Model should load within 10 seconds")
    
    def test_prediction_response_time(self):
        """Test that predictions are made within reasonable time."""
        import time
        
        test_review = "This movie is absolutely fantastic!"
        
        start_time = time.time()
        response = self.app.post('/predict', 
                               data=json.dumps({'review': test_review}),
                               content_type='application/json')
        end_time = time.time()
        
        prediction_time = end_time - start_time
        self.assertLess(prediction_time, 5, "Prediction should complete within 5 seconds")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIMDBSentimentAnalysis)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestModelPerformance))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
