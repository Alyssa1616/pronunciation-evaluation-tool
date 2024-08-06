import requests
import librosa
from io import BytesIO
from pydub import AudioSegment
import io
import re

phoneme_dict = {
    'ɑː', 'ɔː', 'aʊ', 'ɑʊ','ɑi', 'tʃ', 'eɪ','ɛː', 'ɜː','ɛi', 'iː','dʒ', 'oʊ', 'oː', 'ɔi', 'ɔː', 'uː'
}

def load_audio(url):
    response = requests.get(url, stream=True)
    audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format='webm')

    wav_data = 'output.wav'
    audio_segment.export(wav_data, format='wav')
    
    speech, _ = librosa.load(wav_data, sr=16000)
    return speech

def parse_words(result):
    numGroups = 0
    totalPads = 0
    for el in result:
        if el != '<pad>':
            numGroups += 1
        else: totalPads += 1
    avg = int(totalPads / numGroups)
    phonGroups = ""
    currPad = 0
    for el in result:
        if currPad == avg+5:
            phonGroups += " "
        if el != '<pad>':
            phonGroups += el
            currPad = 0
        else:
            currPad += 1


    return re.sub(r' s ', 's ', phonGroups)