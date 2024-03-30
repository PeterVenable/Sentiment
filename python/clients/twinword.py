from typing import Optional

from clients import GenericTextClassificationClient


class TwinWordClient(GenericTextClassificationClient):
    """
    see https://rapidapi.com/twinword/api/sentiment-analysis/
    """
    example_settings = {
        "class": "TwinWordClient",
        "url": "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "YOUR_API_KEY",
            "X-RapidAPI-Host": "twinword-sentiment-analysis.p.rapidapi.com"
        },
        "method": "post",
        "timeout": 5
      }

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
