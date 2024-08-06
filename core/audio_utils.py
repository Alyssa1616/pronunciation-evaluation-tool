import requests
import librosa
from io import BytesIO
from pydub import AudioSegment
import io

def load_audio(url):
    response = requests.get(url, stream=True)
    audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format='webm')

    wav_data = 'output.wav'
    audio_segment.export(wav_data, format='wav')
    
    speech, _ = librosa.load(wav_data, sr=16000)
    return speech