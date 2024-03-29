import json
import logging

from flask import Flask, request, Response
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
    <ul>
    <li>Endpoint: <code>/sentiment</code></li>
    <li>Method: <code>POST</code></li>
    <li>Body: text to classify</li>
    <li>MIME type: <code>text/plain</code></li>
    <li>Response: `200` with sentiment score from -1.0 (most negative) to 1.0 (most positive)</li>
    </ul>
    </body>
    </html>"""


@app.post("/sentiment")
def sentiment():
    data = request.data.decode("utf-8")
    if not data:
        if request.mimetype != "text/plain":
            return "Unsupported media type, please use: text/plain", 415
        return "No data", 400
    score = back_end.classify(data)
    logging.info(f"classified {score:.3f} {json.dumps(data)}")
    return Response(f"{score:.3f}", mimetype="text/plain")
