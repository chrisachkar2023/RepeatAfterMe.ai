from transformers import pipeline
import pronouncing
import difflib
import librosa

asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")

def load_audio(path):
    audio, _ = librosa.load(path, sr=16000)
    return audio

def transcribe(audio):
    result = asr(audio)
    return result['text'].lower().strip()

def words_to_phonemes(word):
    phones = pronouncing.phones_for_word(word)
    return phones[0] if phones else ""

def phoneme_similarity(target_phonemes, transcribed_phonemes):
    similarity = difflib.SequenceMatcher(None, target_phonemes.split(), transcribed_phonemes.split())
    return similarity.ratio()

def evaluate(audio_path, target_word):
    audio = load_audio(audio_path)
    transcription = transcribe(audio)

    target_phonemes = words_to_phonemes(target_word.lower())
    transcribed_phonemes = words_to_phonemes(transcription)

    if not target_phonemes or not transcribed_phonemes:
        score = difflib.SequenceMatcher(None, target_word.lower(), transcription).ratio()
    else:
        score = phoneme_similarity(target_phonemes, transcribed_phonemes)

    return {
        "transcription": transcription,
        "score": round(score, 3)
    }

if __name__ == "__main__":
    file_audio = "/Users/sumankrishna/Desktop/RepeatAfterMe.ai/banayna.m4a"
    target_word = "banana"
    result = evaluate(file_audio, target_word)
    print("Transcribed:", result["transcription"])
    print("Pronunciation score:", result["score"])
