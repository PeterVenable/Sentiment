from clients import GenericTextClassificationClient


class TwinWordClient(GenericTextClassificationClient):
    """
    see https://rapidapi.com/twinword/api/sentiment-analysis/
    The TwinWord API is compatible with the GenericTextClassificationClient, so no overrides are needed.
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
