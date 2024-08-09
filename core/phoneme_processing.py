from flask import Flask
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import re
from io import BytesIO
from transformers import AutoModel, AutoTokenizer 
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import numpy as np
import os
import io
from pydub import AudioSegment
import soundfile as sf
# from transformers import DonutProcessor, VisionEncoderDecoderModel
# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
# from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification
# from core.audio_utils import load_audio, parse_words
from dotenv import load_dotenv
import librosa

def load_audio(url):
    # # buffer = io.BytesIO(file_stream.read())
    # speech, _ = librosa.load(file_path, sr=16000)  # you can adjust the sample rate as needed
    # return speech
    # response = requests.get(url, stream=True)
    # audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format='webm')

    # wav_data = 'output.wav'
    # audio_segment.export(wav_data, format='wav')

    audio_segment = AudioSegment.from_file(url)
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)  # Reset stream position

    speech, _ = librosa.load(wav_io, sr=16000)
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

def recognize_speech_logic(url):

    # Load the phoneme model configuration
    # load_dotenv()
    # hf_token = os.getenv('HF_TOKEN')
    hf_token = "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"
    phoneme_model_name = "facebook/wav2vec2-lv-60-espeak-cv-ft"
    phoneme_model = Wav2Vec2ForCTC.from_pretrained(phoneme_model_name, token=hf_token)
    phoneme_tokenizer = Wav2Vec2Tokenizer.from_pretrained(phoneme_model_name, token=hf_token)

    speech = load_audio(url)

    if speech.ndim > 1:
        speech = speech.mean(axis=1)

    # Tokenize the audio input
    input_values = phoneme_tokenizer(speech, return_tensors="pt").input_values

    # Perform phoneme transcription
    with torch.no_grad():
        logits = phoneme_model(input_values).logits

    vocab = phoneme_tokenizer.get_vocab()
    id_to_token = {id: token for token, id in vocab.items()}

    predicted_ids = torch.argmax(logits, dim=-1)

    phoneme_sequence = [id_to_token[idx.item()] for idx in predicted_ids[0] if idx.item() in id_to_token]
    
    # group the phonemes into words by the spaces between them
    try:
        start_idx = next(i for i, x in enumerate(phoneme_sequence) if x != '<pad>')
        end_idx = len(phoneme_sequence) - next(i for i, x in enumerate(reversed(phoneme_sequence)) if x != '<pad>')

        result = phoneme_sequence[start_idx:end_idx]
    except:
        print("Error: No words were said.")

    # result = 'kamo estas hɔi'

    phonGroups = parse_words(result)

    response = {
        'status': 'success',
        'message': 'Data received',
        'transcription': phonGroups,
    }
    
    return jsonify(response)