from flask import Flask, request, jsonify, render_template
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Automatically render index.html on page load

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    body = str.encode(json.dumps({"Inputs": {"input1": [data]}, "GlobalParameters": {}}))

    url = 'https://ac53101f-0356-4de0-bfb5-83276dd7e6ad.eastus2.azurecontainer.io/score'
    api_key = 'OfdoyWgPCQmGmCiHshjrmFgXc4mPsh9E'
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        return jsonify(result)
    except urllib.error.HTTPError as error:
        return jsonify({"error": error.code, "message": error.read().decode("utf8", 'ignore')})


if __name__ == '__main__':
    app.run(debug=True)