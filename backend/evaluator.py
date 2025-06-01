from transformers import pipeline
import pronouncing
import difflib
import librosa

# initialize automatic speech recognition (ASR) pipeline
asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")

# loads audio file
def load_audio(path):
    audio, _ = librosa.load(path, sr=16000) # change sample rate per model
    return audio

# uses ASR pipeline to transcribe audio
def transcribe(audio):
    result = asr(audio)
    return result['text'].lower().strip()

# looks up phoneme spelling of a word
def words_to_phonemes(word):
    phones = pronouncing.phones_for_word(word)
    return phones[0] if phones else ""

# calculates similiarty ratio between the target and transcribed phonemes
def phoneme_similarity(target_phonemes, transcribed_phonemes):
    similarity = difflib.SequenceMatcher(None, target_phonemes.split(), transcribed_phonemes.split())
    return similarity.ratio()

# evaluates pronouncation
def evaluate(audio_path, target_word):
    # load audio and run speech recognition
    audio = load_audio(audio_path)
    transcription = transcribe(audio)

    # convert both to phonemes
    target_phonemes = words_to_phonemes(target_word.lower())
    transcribed_phonemes = words_to_phonemes(transcription)

    # use phoneme similary if possible, otherwise text comparison
    if not target_phonemes or not transcribed_phonemes:
        score = difflib.SequenceMatcher(None, target_word.lower(), transcription).ratio()
    else:
        score = phoneme_similarity(target_phonemes, transcribed_phonemes)

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