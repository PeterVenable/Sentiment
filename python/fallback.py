import logging
import time
from typing import Optional

from sentiment_classifier import SentimentClassifier, ClassifierError, ClassifierServiceFailureError


class FallBackSentimentClassifier(SentimentClassifier):
    """
    Use one method to classify text, falling back to a second if the first fails.
    After failure, retry the primary method after a set time.
    """
    def __init__(self,
                 primary: SentimentClassifier,
                 secondary: SentimentClassifier,
                 retry_after: (int | float) = 10,
                 increase_retry: (int | float) = 10,
                 max_wait: (int | float) = 600,
                 ):
        """
        :param primary: the primary classifier
        :param secondary: the backup classifier
        :param retry_after: seconds to wait before using the primary classifier again after a failure
        :param increase_retry: seconds to increase retry_after by following each failure
        :param max_wait: maximum time to wait before retrying the primary classifier (i.e. stop increasing)
        """
        super().__init__()
        self.primary = primary
        self.secondary = secondary
        self.max_wait = max(0, max_wait)
        self.retry_after = max(0, min(retry_after, self.max_wait))
        self.increase_retry = max(0, min(increase_retry, self.max_wait))
        self.next_retry_: Optional[float] = None
        self.failure_count_ = 0

    def classify(self, text: str) -> float:
        """
        Classify text using the primary classifier, falling back to the secondary if the primary fails.
        :param text: the text string to classify
        :return: a score from -1 to 1
        """
        self.count += 1
        score = None
        if self.next_retry_ is not None and time.time() >= self.next_retry_:
            logging.info("Re-trying primary classifier after failure")
            self.next_retry_ = None
        if self.next_retry_ is None:
            try:
                score = self.primary.classify(text)
            except ClassifierServiceFailureError:
                pass
            if score is None:
                logging.warning("Primary classifier failed, falling back to secondary")
                self.next_retry_ = time.time() + self.retry_after
                self.retry_after = min(self.retry_after + self.increase_retry, self.max_wait)
                self.failure_count_ += 1
        if score is None:
            score = self.secondary.classify(text)
            if score is None:
                raise ClassifierError("Both classifiers failed")
        return score
