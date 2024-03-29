from typing import Optional


class ClassifierError(Exception):
    """
    An error occurred while classifying text.
    """


class SentimentClassifier:
    """
    A sentiment classifier rates the sentiment of text.
    Sentiment is classified as a score from -1.0 (most negative) to 1.0 (most positive).
    This is an abstract class that must be subclassed to implement the classify method.
    """
    def __init__(self):
        self.count = 0  # the number of times classify() has been called

    def classify(self, text: str) -> Optional[float]:
        """
        Classify text and return a sentiment score from -1 to 1.
        :param text: text to classify
        :return: a sentiment score from -1.0 (most negative) to 1.0 (most positive) or None on failure
        """
        raise NotImplementedError()
