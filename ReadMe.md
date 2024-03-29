# Sentiment

This is a WSGI web application that analyses the sentiment of short text strings.

It has just one simple endpoint, `/sentiment`, that accepts a POST request with a 
`text/plain` payload of text to analyze. It returns a JSON response with a `score` field
containing a floating point number between -1 and 1.

## Authentication

The service is protected by a very simple Bearer authentication scheme. 
(https://swagger.io/docs/specification/authentication/bearer-authentication/)
For testing, valid tokens can be configured in the `settings.json` file.
For production, you will need to implement your method of acquiring and validating tokens.

## Fallback

The service primarily uses a third-party API to perform sentiment analysis.
However, when that API is unavailable, the service falls back to a local language model.

## Configuration

The service can be configured using the `settings.json` file. 

### client

The `client` section specifies the third-party API to use for sentiment analysis.

It has the following properties:
* `class` - The name of a class that implements the `SentimentClassifier` interface.
    Currently implemented classes are `TwinWordClient` and `ConnexunClient`.
* `url` - The URL of the third-party API sentiment analysis route.
* `headers` - A dictionary of headers to include in the request to the third-party API.
    These typically specify authentication and content type.
* `method` - `"get"` or `"post"`
* `timeout` - The number of seconds to wait for a response from the third-party API.

### model

The `model` section has one property: 
The `name` field specifies the fully-qualified name of a Huggingface model to use locally when the 
third-party API is unavailable.

### fallback

The `fallback` section lets you configure the fallback behavior:
* `retry_after` - The number of seconds to wait before retrying the third-party API after a failure.
* `increase_retry` - The number of seconds to increase the wait time by after each failure.
* `max_wait` - The maximum number of seconds to which the timeout can increase.

### logging

The optional `logging` section lets you configure the logging behavior.

### tokens

The optional `tokens` section lets you configure authentication tokens for testing.
For example, the following tokens:
```json
"tokens": [
    {"client_id": "test", "access_token": "just for testing!"}
  ],
```
will allow a request with the header `Authorization "Bearer test"` to access the service.

### test_csv

The optional `test_csv` path lets you configure a CSV file to use for testing.
Point it to a CSV file with a `text` column, such as the 
[twitter-airline-sentiment](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment)
dataset before running the unit tests.

## Example

Here is an example of a request and response:

PowerShell
```powershell
Invoke-WebRequest -Uri http://localhost:8000/sentiment -Method Post -Body "yes that's AWESOME" -ContentType "text/plain" -Headers @{'Authorization'= 'bearer test'}
```

bash
```bash
curl -X POST http://localhost:8000/sentiment --data "yes that's AWESOME" -H "Content-Type: text/plain" -H 'Authorization: "Bearer test"'
```

Response (200 OK)
```json
{"score":0.9949,"text":"yes that's AWESOME"}
```
