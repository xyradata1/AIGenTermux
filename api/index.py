import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# This would be updated by the admin.py (or a secret)
# For this example, we use a global variable or environment variable
GLOBAL_CONFIG = {
    "api_key": os.environ.get("OPENAI_API_KEY", ""),
    "model": "gpt-4o-mini"
}

@app.route('/get_config', methods=['GET'])
def get_config():
    return jsonify(GLOBAL_CONFIG)

@app.route('/set_config', methods=['POST'])
def set_config():
    # In a real app, you'd want auth here
    data = request.json
    GLOBAL_CONFIG["api_key"] = data.get("api_key", GLOBAL_CONFIG["api_key"])
    GLOBAL_CONFIG["model"] = data.get("model", GLOBAL_CONFIG["model"])
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
