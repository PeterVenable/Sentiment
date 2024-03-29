import json
import re

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax

from sentiment_classifier import SentimentClassifier, ClassifierError, InvalidTextError


class HuggingFaceSentimentClassifier(SentimentClassifier):
    """
    A sentiment classifier that uses a pre-trained model to classify text.
    Text is preprocessed by replacing usernames and URLs with placeholders.
    Sentiment is classified as a score from -1.0 (most negative) to 1.0 (most positive).
    """

    def __init__(self, model: str = "cardiffnlp/twitter-roberta-base-2021-124m-sentiment"):
        super().__init__()
        self._config = AutoConfig.from_pretrained(model)
        self._tokenizer = AutoTokenizer.from_pretrained(model)
        self._model = AutoModelForSequenceClassification.from_pretrained(model)

    def preprocess_(self, text: str) -> str:
        """
        Preprocess Twitter text by replacing usernames and URLs with placeholders.
        :param text: a string of text
        :return: the text with usernames and URLs replaced
        """
        text = re.sub(r"(?<!\w)@\w+", "@user", text)
        text = re.sub(r"\bhttp\S+\b", "http", text)
        return text

    def classify_to_labels_(self, text: str) -> dict[str, float]:
        """
        Classify text using the current model, and return a dict of labels to scores.
        :param text: text to classify
        :return: dict from label to probability
        """
        text = self.preprocess_(text)
        encoded_input = self._tokenizer(text, return_tensors='pt')
        output = self._model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        label_scores = {label: float(scores[i]) for i, label in self._config.id2label.items()}
        return label_scores

    def interpret_score_(self, scores: dict[str, float]) -> float:
        """
        Convert a dict of label scores to a single sentiment score.
        :param scores: dict from label to probability, including "positive" and "negative"
        :return: a sentiment score from -1.0 (most negative) to 1.0 (most positive)
        """
        assert 0.0 <= scores["positive"] <= 1.0
        assert 0.0 <= scores["negative"] <= 1.0
        score = scores["positive"] - scores["negative"]
        return score

    def classify(self, text: str) -> float:
        """
        Classify text and return a sentiment score from -1 to 1.
        :param text: text to classify
        :return: a sentiment score from -1.0 (most negative) to 1.0 (most positive)
        :raises ClassifierError: if an error occurs while classifying the text
        """
        self.count += 1
        if not text:
            raise InvalidTextError("Empty text")
        scores = self.classify_to_labels_(text)
        score = self.interpret_score_(scores)
        if score is None:
            raise ClassifierError(f"Unable to classify text using local model: {json.dumps(text)}")
        return score
