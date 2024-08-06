from flask import request, jsonify
from run import app

@app.route('/labels/', methods=['POST'])
def recognize_speech():
    from .phoneme_processing import recognize_speech_logic
    data = request.get_json()
    url = data['file']
    response = recognize_speech_logic(url)
    return jsonify(response)