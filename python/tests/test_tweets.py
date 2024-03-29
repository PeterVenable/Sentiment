import csv
import unittest


class FlaskTest(unittest.TestCase):

    """
    This tests the app with a CSV file of tweets.
    Only the "text" column of the CSV file is used.
    The path to the CSV file is in settings.json under "test_csv", like this:
    {
        "test_csv": "path/to/Tweets.csv"
    }
    """

    def try_load_tweets(self, limit: int = 200) -> list[str]:
        from settings import settings
        tweets: list[str] = []
        file = settings.get("test_csv")
        if not file:
            return []
        try:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = row["text"]
                    tweets.append(text)
                    if len(tweets) >= limit:
                        break
        except (IOError, KeyError):
            pass
        return tweets

    def test_tweets(self):
        tweets = self.try_load_tweets()
        if not tweets:
            raise RuntimeError("""This test requires the settings to contain "testing": "path/to/Tweets.csv".""")
        from wsgi import app  # import the Flask app
        self.app = app.test_client()
        self.app.testing = True
        for tweet in tweets:
            self._test_tweet(tweet)

    headers = {
        "Authorization": "Bearer test",
        "Content-Type": "text/plain",
    }

    def _test_tweet(self, text: str):
        response = self.app.post('/sentiment', data=text, headers=self.headers)
        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertIsInstance(data.get("score"), float)
        self.assertEqual(text, data.get("text"))
