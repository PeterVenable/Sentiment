import unittest


class FlaskTest(unittest.TestCase):

    text_positive = "what a sunny day for a walk"
    text_negative = "worst day of my LIFE"

    def setUp(self):
        from wsgi import app  # import the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sentiment API', response.data)

    def test_no_headers(self):
        headers = {}
        response = self.app.post('/sentiment', data=self.text_positive, headers=headers)
        self.assertEqual(401, response.status_code)

    def test_no_authorization(self):
        headers = {
            "Content-Type": "text/plain",
        }
        response = self.app.post('/sentiment', data=self.text_positive, headers=headers)
        self.assertEqual(401, response.status_code)

    def test_wrong_authorization_type(self):
        headers = {
            "Content-Type": "text/plain",
            "Authorization": "Basic foo",
        }
        response = self.app.post('/sentiment', data=self.text_positive, headers=headers)
        self.assertEqual(401, response.status_code)

    def test_wrong_authorization_key(self):
        headers = {
            "Content-Type": "text/plain",
            "Authorization": "Bearer wrong",
        }
        response = self.app.post('/sentiment', data=self.text_positive, headers=headers)
        self.assertEqual(401, response.status_code)

    def test_positive(self):
        headers = {
            "Authorization": "Bearer test",
            "Content-Type": "text/plain",
        }
        response = self.app.post('/sentiment', data=self.text_positive, headers=headers)
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertGreaterEqual(data.get("score"), 0.8)

    def test_negative(self):
        headers = {
            "Authorization": "Bearer test",
            "Content-Type": "text/plain",
        }
        response = self.app.post('/sentiment', data=self.text_negative, headers=headers)
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertLessEqual(data.get("score"), -0.8)
