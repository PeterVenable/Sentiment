import requests
from typing import Optional

from sentiment_classifier import (
    SentimentClassifier, ClassifierError, ClassifierServiceFailureError, InvalidTextError)


class GenericTextClassificationClient(SentimentClassifier):
    """
    Generic client for sentiment analysis services.
    Use a subclass for a specific service, to correctly format the query and interpret the response.
    Each subclass should override the format_query() and extract_result() methods.
    """
    def __init__(self, *,
                 url: str,
                 headers: dict[str, str],
                 method: str = "post",
                 timeout: int = 5,
                 ):
        """
        Generic client for sentiment analysis services.
        Use a subclass for a specific service, to correctly format the query and interpret the response.

        :param url: the full URL for service requests
        :param headers: headers to include with each request
        :param method: "get" or "post"
        :param timeout: timeout in seconds
        """
        super().__init__()
        self._url = url
        self._headers = headers
        self._method = method.lower()
        self._timeout = timeout
        if self._method not in ("get", "post"):
            raise ValueError(f"Unsupported method: {self._method}")

    def classify(self, text: str) -> float:
        self.count += 1
        if not text:
            raise InvalidTextError("Empty text")
        querystring = self.format_query(text)
        try:
            data = self._request(querystring)
        except OSError as e:
            raise ClassifierServiceFailureError(e)
        score = self.extract_result(data)
        if isinstance(score, int):
            score = float(score)
        elif not isinstance(score, float):
            raise ClassifierError(f"Invalid score: {score}")
        return score

    def _request(self, data: object) -> dict:
        if self._method == "get":
            response = requests.get(
                url=self._url, headers=self._headers, params=data, timeout=self._timeout)
        elif self._method == "post":
            response = requests.post(
                url=self._url, headers=self._headers, data=data, timeout=self._timeout)
        else:
            raise ValueError(f"Unsupported method: {self._method}")
        if response.status_code != 200:
            raise ClassifierServiceFailureError(
                f"Classification request failed with HTTP status: {response.status_code}")
        return response.json()

    def format_query(self, text: str) -> object:
        """
        Convert the text to a format suitable for the service.
        :param text: the text to classify
        :return: object or text suitable for the service API
        """
        return {"text": text}

    def extract_result(self, data: dict) -> Optional[float]:
        """
        Extract the sentiment score from the service response.
        :param data: JSON response from the service
        :return: the score as a float, or None if not found
        """
        return data.get("score")
