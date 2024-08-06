from flask import Flask, request, jsonify
from flask_cors import CORS
from core.phoneme_processing import recognize_speech_logic

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/recognize/', methods=['POST'])
def recognize_speech():
    data = request.get_json()
    url = data['file']
    response = recognize_speech_logic(url)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)