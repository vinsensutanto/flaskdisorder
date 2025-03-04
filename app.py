from flask import Flask, request, jsonify, render_template
import urllib.request
import json
import os
import ssl
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def allowSelfSignedHttps(allowed=True):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)  # Call this once outside

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Empty JSON payload"}), 400
        
        logging.debug(f"Incoming Data: {request.data}")
        logging.debug(f"Headers: {request.headers}")

        body = str.encode(json.dumps({"Inputs": {"input1": [data]}, "GlobalParameters": {}}))

        url = 'https://ac53101f-0356-4de0-bfb5-83276dd7e6ad.eastus2.azurecontainer.io/score'
        api_key = 'OfdoyWgPCQmGmCiHshjrmFgXc4mPsh9E'  
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        result_data = result["Results"]["WebServiceOutput0"][0]
        scored_label = result_data["Scored Labels"]
        probabilities = {key.replace("Scored Probabilities_", ""): round(value * 100, 2) for key, value in result_data.items() if key.startswith("Scored Probabilities")}
        
        return jsonify({"Scored Label": scored_label, "Probabilities": probabilities})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Izinin semua origin
    
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500
