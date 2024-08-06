from flask import Flask
from flask_cors import CORS
from server.core.phoneme_controller import recognize_speech

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.add_url_rule('/recognize/', view_func=recognize_speech, methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)