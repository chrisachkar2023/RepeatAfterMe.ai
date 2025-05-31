from transformers import pipeline
import difflib
import librosa

# initializes automatic speech recognition (ASR) pipeline
asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")

# loads audio file
def load_audio(path):
    audio, _ = librosa.load(path, sr=16000)
    return audio

# uses ASR pipeline to transcribe audio
def transcribe(audio):
    result = asr(audio)
    return result['text'].lower().strip()

# compute similarity ratio between expected and transcribed text
def get_score(target_text, transcribed_text):
    similarity = difflib.SequenceMatcher(None, target_text, transcribed_text)
    return similarity.ratio()

# scores pronunciation
def evaluate(audio, target_text):
    audio = load_audio(audio)
    transcription = transcribe(audio)
    score = get_score(target_text.lower(), transcription)
    return {
        "transcription": transcription,
        "score": round(score, 3)  
    }

# main
file_audio = "/Users/Christopher/Desktop/banana.m4a"
target_word = "banana"
result = evaluate(file_audio, target_word)

print("Transcribed:", result["transcription"])
print("Pronunciation score:", result["score"])