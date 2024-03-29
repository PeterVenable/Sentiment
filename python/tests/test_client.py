import unittest


class ClientClassifyTestCase(unittest.TestCase):
    def setUp(self):
        from setup import get_remote_client
        self.client = get_remote_client()

    def _get_score(self, text: str) -> float:
        score = self.client.classify(text)
        self.assertIsInstance(score, float)
        self.assertLessEqual(-1.0, score)
        self.assertLessEqual(score, 1.0)
        return score

    def test_positive(self):
        score = self._get_score("I love this product")
        self.assertLess(0.9, score)

    def test_negative(self):
        score = self._get_score("I hate this product")
        self.assertLess(score, -0.9)

    def test_neutral(self):
        score = self._get_score("Today is Tuesday, and the weather forecast predicts partly cloudy skies with a chance of rain in the afternoon.")
        self.assertLess(-0.5, score)
        self.assertLess(score, 0.5)

    def test_aargh(self):
        self._get_score("AAAARGH why is this happening")
