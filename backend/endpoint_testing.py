import unittest
import json
from app import app  # Replace `app` with the name of your Flask app module if different


class TestQueryEndpoint(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.client = app.test_client()
        self.client.testing = True

    def test_query_with_valid_question(self):
        # Test with a valid question
        response = self.client.post(
            '/query',
            data=json.dumps({"question": "What is the capital of France?"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.json)

    def test_query_with_missing_question(self):
        # Test when "question" is missing
        response = self.client.post(
            '/query',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "No question provided")

    def test_query_with_empty_question(self):
        # Test when "question" is an empty string
        response = self.client.post(
            '/query',
            data=json.dumps({"question": ""}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "No question provided")

    def test_query_with_server_error(self):
        # Test handling a server error
        with app.test_client() as client:
            # Mock `query_model` to raise an exception
            app.view_functions['handle_query'].__globals__['query_model'] = lambda x: (_
                                                                                       for
                                                                                       _
                                                                                       in
                                                                                       ()).throw(
                Exception("Mocked server error"))

            response = client.post(
                '/query',
                data=json.dumps({"question": "What is 2 + 2?"}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json)
            self.assertEqual(response.json['error'], "Mocked server error")


if __name__ == '__main__':
    unittest.main()
