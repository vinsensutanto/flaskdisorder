from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import ssl
import urllib.request
import json

app = Flask(__name__, template_folder='templates')

CORS(app)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

@app.route('/')
def index():
    return render_template('index.html')  # Serve HTML Here

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        body = str.encode(json.dumps({"Inputs": {"input1": [data]}, "GlobalParameters": {}}))

        url = 'https://ac53101f-0356-4de0-bfb5-83276dd7e6ad.eastus2.azurecontainer.io/score'
        api_key = 'OfdoyWgPCQmGmCiHshjrmFgXc4mPsh9E'
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        return jsonify(result)

    except urllib.error.HTTPError as error:
        return jsonify({"error": error.code, "message": error.read().decode("utf8", 'ignore')})
    
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 🔥 Default to 5000 if no PORT env
    app.run(debug=True, host="0.0.0.0", port=port)
