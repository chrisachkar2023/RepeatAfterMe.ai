from transformers import pipeline
import pronouncing
import difflib
from pydub import AudioSegment
import numpy as np

# initialize automatic speech recognition (ASR) pipeline
asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")

# loads input audio
def load_audio(unprocessed_audio):
    audio = AudioSegment.from_file(unprocessed_audio)
    audio = audio.set_channels(1).set_frame_rate(16000) # change rate per model
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= 32768.0
    return samples

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
    transcription = transcribe(audio).replace(" ", "")

    # convert both to phonemes
    target_phonemes = words_to_phonemes(target_word.lower())
    transcribed_phonemes = words_to_phonemes(transcription)

    # use phoneme similarity if possible, otherwise text comparison
    if not target_phonemes or not transcribed_phonemes:
        score = difflib.SequenceMatcher(None, target_word.lower(), transcription).ratio()
    else:
        score = phoneme_similarity(target_phonemes, transcribed_phonemes)

    return {
        "transcription": transcription,
        "score": f"{round(score * 100, 2)}%"
    }