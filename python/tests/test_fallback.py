import time
import unittest

from sentiment_classifier import SentimentClassifier, ClassifierServiceFailureError
from fallback import FallBackSentimentClassifier
from setup import get_local_classifier


class FailureTestClassifier(SentimentClassifier):
    def __init__(self, classifier: SentimentClassifier):
        super().__init__()
        self._classifier = classifier

    def classify(self, text: str) -> float:
        case_ = self.count % 8
        self.count += 1
        if case_ == 2:
            raise ClassifierServiceFailureError("Test failure")
        if case_ == 4:
            raise ClassifierServiceFailureError("Test failure")
        return self._classifier.classify(text)


class FallbackClassifyTestCase(unittest.TestCase):

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
        primary = get_local_classifier()
        secondary = get_local_classifier()
        failure_client = FailureTestClassifier(primary)
        fallback = FallBackSentimentClassifier(primary=failure_client, secondary=secondary, retry_after=30)
        for text in self.texts:
            score = fallback.classify(text)
            self.assertIsInstance(score, float)
        self.assertEqual(1, fallback.failure_count_)
        self.assertEqual(3, failure_client.count)
        self.assertEqual(2, primary.count)
        self.assertEqual(len(self.texts) - 2, secondary.count)

    def test_fallback_with_delay(self):
        primary = get_local_classifier()
        secondary = get_local_classifier()
        failure_client = FailureTestClassifier(primary)
        delay = 0.5
        fallback = FallBackSentimentClassifier(
            primary=failure_client, secondary=secondary,
            retry_after=delay, increase_retry=delay, max_wait=5*delay)
        for index, text in enumerate(self.texts):
            score = fallback.classify(text)
            self.assertIsInstance(score, float, msg=text)
            time.sleep(delay)
        self.assertEqual(3, secondary.count)
        self.assertEqual(2, fallback.failure_count_)
        self.assertEqual(len(self.texts) - 1, failure_client.count)
        self.assertEqual(len(self.texts) - 3, primary.count)
