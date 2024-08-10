from flask import Flask, request, jsonify
from flask_cors import CORS
from core.phoneme_processing import recognize_speech_logic
from werkzeug.utils import secure_filename
import os
import base64
import io
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*", "http://localhost:3000"]}})
app.config['CORS_HEADERS'] = 'Content-Type'

hf_token = "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"
phoneme_model_name = "facebook/wav2vec2-lv-60-espeak-cv-ft"
phoneme_model = Wav2Vec2ForCTC.from_pretrained(phoneme_model_name, token=hf_token)
phoneme_tokenizer = Wav2Vec2Tokenizer.from_pretrained(phoneme_model_name, token=hf_token)

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
    # return jsonify("Recognition result")
    print("0")
    # data = request.get_json()
    # url = data['file']

    # print("0.1")
    # audio_base64 = data['file']
        
    # if audio_base64.startswith('data:'):
    #     audio_base64 = audio_base64.split(',')[1]
    
    # audio_data = base64.b64decode(audio_base64)
        
    # audio_io = io.BytesIO(audio_data)
    
    # response = recognize_speech_logic("new_test1.wav", phoneme_tokenizer, phoneme_model)
    return "hello"

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 105))
#     app.run(host='0.0.0.0', port=port)