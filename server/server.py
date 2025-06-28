from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from server import util
import os
import base64

app = Flask(__name__, static_folder="../UI", static_url_path="/")
CORS(app)

# ✅ Load model when the server starts (always, even in Gunicorn)
util.load_saved_artifacts()

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'app.html')

@app.route('/classify_image', methods=['POST'])
def classify_image():
    try:
        if 'file' not in request.files:
            print("❌ No file part in request.")
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        print("✅ File received:", file.filename)

        # Convert image to base64
        image_data = base64.b64encode(file.read()).decode('utf-8')
        image_data = 'data:image/jpeg;base64,' + image_data

        # Classify using util
        print("🔍 Calling classifier...")
        result = util.classify_image(image_data)
        print("🎯 Classification result:", result)

        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print("❌ Error during classification:", str(e))
        return jsonify({'error': str(e)}), 500
