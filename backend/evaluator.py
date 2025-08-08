from transformers import pipeline
import numpy as np
from g2p_en import G2p
import pronouncing
from panphon.distance import Distance
from pydub import AudioSegment
import google.generativeai as genai
import os

# Initialize Pipeline
asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")
g2p = G2p()
d = Distance()

# set up gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Load and preprocess audio
def load_audio(file_obj):
    audio = AudioSegment.from_file(file_obj)
    audio = audio.set_channels(1).set_frame_rate(16000)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= 32768.0
    return samples

def transcribe(audio):
    result = asr(audio)
    return result['text'].strip().lower()

# Convert any word into phonemes
def words_to_phonemes(word):
    phones = pronouncing.phones_for_word(word)
    if phones:
        return phones[0]  
    else:
        return generate_phonemes(word)  

# G2P fallback for unknown/garbled words
def generate_phonemes(text):
    g2p_output = g2p(text)
    return " ".join([p for p in g2p_output if p.strip() and not p.isspace()])

# Compare phoneme similarity using normalized Levenshtein
def phoneme_similarity(target_phonemes, transcribed_phonemes):
    dist = d.levenshtein_distance(target_phonemes, transcribed_phonemes)
    max_len = max(len(target_phonemes.split()), 1)
    similarity = max(0.0, 1 - dist / max_len)
    return similarity

# Full evaluation
def evaluate(audio_path, target_word, logged_in):
    audio = load_audio(audio_path)
    transcription = transcribe(audio).replace(" ", "")
    
    # Phoneme conversion
    target_phonemes = words_to_phonemes(target_word.lower())
    transcribed_phonemes = generate_phonemes(transcription)

    if not target_phonemes or not transcribed_phonemes:
        score = 0.0
    else:
        score = phoneme_similarity(target_phonemes, transcribed_phonemes)

    percentage = round(score * 100, 2)
    
    if percentage <= 20:
        feedback = "Bad Pronouncation"
    elif percentage <= 50:
        feedback = "Okay Pronouncation"
    elif percentage <= 75:
        feedback = "Good Pronouncation"
    else:
        feedback = "Perfect Pronouncation" 
        
    # disable AI feedback when signed out or when perfect pronouncation
    if not logged_in:
        ai_feedback = "Please login to use AI feedback."
    elif percentage > 75:
        ai_feedback = "No feedback needed — perfect pronunciation!"
    else:
        ai_feedback = generate_pronunciation_feedback(score, transcription, target_word)   

    return {
        "target_word": target_word,
        "transcription": transcription,
        "feedback": feedback,
        "score": f"{round(score * 100, 2)}%",
        "ai_feedback": ai_feedback
    }

# uses gemini api for ai feedback
def generate_pronunciation_feedback(score: float, transcription: str, target_word: str):
    model = genai.GenerativeModel("gemma-3-27b-it")
    
    prompt = (
        f"Give a very brief (2 sentences max) constructive feedback on the pronunciation of '{target_word}'. "
        f"The user's transcription is '{transcription}' with a similarity score of {round(score * 100, 2)}%."
    )

    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 100,
            "temperature": 0.7
        }
    )

    # failsafe if we make too many API calls
    if not response.text:
        return "AI feedback unavailable. Please try again later."
    
    return response.text