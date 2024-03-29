import json
from typing import Optional

from clients import GenericTextClassificationClient


class ConnexunClient(GenericTextClassificationClient):
    """
    See https://rapidapi.com/connexun-srl-connexun-srl-default/api/sentiments1/
    """
    example_settings = {
        "class": "TwinWordClient",
        "url": "https://sentiments1.p.rapidapi.com/sentiment",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "YOUR_API_KEY",
            "X-RapidAPI-Host": "sentiments1.p.rapidapi.com"
        },
        "method": "post",
        "timeout": 5
      }

    def format_query(self, text: str) -> object:
        return json.dumps({"text": text})

    def extract_result(self, data: dict) -> Optional[float]:
        sentiment = data.get("Sentiment")
        probability = data.get("Value")
        if not isinstance(probability, float):
            return None
        if sentiment == "positive":
            return probability
        elif sentiment == "negative":
            return -probability
        else:
            return None
