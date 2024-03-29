import unittest


class LocalModelClassifyTestCase(unittest.TestCase):
    def setUp(self):
        from huggingface import HuggingFaceSentimentClassifier
        from settings import settings
        try:
            kwargs = {"model": settings["model"]["name"]}
        except (KeyError, TypeError):
            kwargs = {}
        self.classifier = HuggingFaceSentimentClassifier(**kwargs)

    def _get_score(self, text: str) -> float:
        score = self.classifier.classify(text)
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
        score = self._get_score(
            "Today is Tuesday, and the weather forecast predicts partly cloudy skies with a chance of rain.")
        self.assertLess(-0.5, score)
        self.assertLess(score, 0.5)

    def test_preprocess(self):
        score1 = self._get_score("@dude, check out this link: https://example.com/foobar")
        score2 = self._get_score("@mann, check out this link: http://example.com/hashbaz")
        self.assertEqual(score1, score2)

    def test_aargh(self):
        self._get_score("AAAARGH why is this happening")
