import unittest


class ClientClassifyTestCase(unittest.TestCase):
    def setUp(self):
        from settings import settings
        import clients
        client_settings = settings["client"]
        class_name = client_settings["class"]
        # import the class from the client module
        klass = getattr(clients, class_name, None)
        if not issubclass(klass, clients.GenericTextClassificationClient):
            raise ValueError(f"Unsupported client: {class_name}")
        self.client = klass(
            url=client_settings["url"],
            headers=client_settings["headers"],
            method=client_settings["method"],
            timeout=int(client_settings.get("timeout", 5)),
        )

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
