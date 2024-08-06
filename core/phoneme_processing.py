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
from pydub import AudioSegment
import soundfile as sf
from transformers import DonutProcessor, VisionEncoderDecoderModel
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification
from .audio_utils import load_audio, parse_words
from dotenv import load_dotenv

def recognize_speech_logic(url):

    # Load the phoneme model configuration
    load_dotenv()
    hf_token = os.getenv('HF_TOKEN')
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