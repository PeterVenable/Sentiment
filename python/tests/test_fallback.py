import time
import unittest
from typing import Optional

from fallback import FallBackSentimentClassifier
from sentiment_classifier import SentimentClassifier
from huggingface import HuggingFaceSentimentClassifier
from settings import settings
import clients


class FailureTestClassifier(SentimentClassifier):
    def __init__(self, classifier: SentimentClassifier):
        super().__init__()
        self._classifier = classifier

    def classify(self, text: str) -> Optional[float]:
        case_ = self.count % 8
        self.count += 1
        if case_ == 2:
            raise IOError("Test failure")
        if case_ == 4:
            return None
        if case_ == 6:
            raise TimeoutError("Test timeout")
        return self._classifier.classify(text)


class FallbackClassifyTestCase(unittest.TestCase):
    def setUp(self):
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
        try:
            kwargs = {"model": settings["model"]["name"]}
        except (KeyError, TypeError):
            kwargs = {}
        self.classifier_kwargs = kwargs

    texts = [
        "I love this product",
        "I hate this product",
        "mY FLIGTH IS DELAYED",
        "AAAARGH why is this happening",
        "actually something good happened today",
        "I'm so happy",
        "where are the peanuts?",
        "I'm so tired",
        "so many interesting people and sitting around doing nothing",
    ]

    def test_fallback_no_delay(self):
        classifier = HuggingFaceSentimentClassifier(**self.classifier_kwargs)
        failure_client = FailureTestClassifier(self.client)
        fallback = FallBackSentimentClassifier(primary=failure_client, secondary=classifier)
        for text in self.texts:
            score = fallback.classify(text)
            self.assertIsInstance(score, float)
        self.assertEqual(fallback.failure_count_, 1)
        self.assertEqual(failure_client.count, 3)
        self.assertEqual(classifier.count, len(self.texts) - 2)

    def test_fallback_with_delay(self):
        classifier = HuggingFaceSentimentClassifier(**self.classifier_kwargs)
        failure_client = FailureTestClassifier(self.client)
        fallback = FallBackSentimentClassifier(
            primary=failure_client, secondary=classifier,
            retry_after=1, increase_retry=1, max_wait=5)
        for index, text in enumerate(self.texts):
            score = fallback.classify(text)
            self.assertIsInstance(score, float, msg=text)
            time.sleep(1)
        self.assertEqual(classifier.count, 5)
        self.assertEqual(fallback.failure_count_, 3)
        self.assertEqual(failure_client.count, len(self.texts) - 2)
