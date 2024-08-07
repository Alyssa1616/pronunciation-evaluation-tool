from flask import Flask, request, jsonify
from flask_cors import CORS
from core.phoneme_processing import recognize_speech_logic
from werkzeug.utils import secure_filename
import os
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({"message": "API is up and running!"})

@app.route('/recognize', methods=['POST', 'HEAD'])
def recognize_speech():
    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file part'}), 400
    # file = request.files['file']
    # if file.filename == '':
    #     return jsonify({'error': 'No selected file'}), 400

    # # Read file into BytesIO stream
    # file_stream = io.BytesIO()
    # file.save(file_stream)
    # file_stream.seek(0)
    data = request.get_json()
    url = data['file']
    response = recognize_speech_logic(url)
    return jsonify(response)

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 105))
#     app.run(host='0.0.0.0', port=port)