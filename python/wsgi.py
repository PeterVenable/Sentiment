import json
import logging

from flask import Flask, request, jsonify

from sentiment_classifier import ClassifierError
from setup import get_fallback_classifier, configure_logging


"""
set up the web server
"""
configure_logging()
app = Flask(__name__)
app.config.update(
    MAX_CONTENT_LENGTH=4096,
)
back_end = get_fallback_classifier()


@app.route("/")
def overview():
    return """<html><head><title>Sentiment</title></head>
    <body>
    <h1>Sentiment API</h1>
    <p>This API provides sentiment analysis for text.</p>
    <h2>/sentiment</h2>
    <h3>Request</h3>
    <ul>
    <li>Endpoint: <code>/sentiment</code></li>
    <li>Method: <code>POST</code></li>
    <li>Body: text to classify</li>
    <li>MIME type: <code>text/plain</code></li>
    </ul>
    <h3>Response</h3>
    On success, the response is a `200` with a JSON object with the following fields:
    <ul>
    <li><code>score</code>: sentiment score from -1.0 (most negative) to 1.0 (most positive)</li>
    <li><code>text</code>: the text that was classified</li>
    </ul>
    On error, the response is a non-`200` status code with a JSON object with the following fields:
    <ul>
    <li><code>error</code>: a description of the error</li>
    <li><code>text</code>: the text that was not classified</li>
    </ul>
    </body>
    </html>"""


@app.post("/sentiment")
def sentiment():
    text = request.data.decode("utf-8")
    error = ""
    code = 200
    score = 0.0
    if not text:
        if request.mimetype != "text/plain":
            error, code = "Unsupported media type, please use: text/plain", 415
        else:
            error, code = "No data", 400
    if not error:
        try:
            score = back_end.classify(text)
        except ClassifierError as e:
            error, code = f"{e}", 400
    if error:
        logging.error(error)
        result = {"error": error, "text": text}
    else:
        logging.info(f"classified {score:.3f} {json.dumps(text)}")
        result = {"score": round(score, 5), "text": text}
    return jsonify(result), code
