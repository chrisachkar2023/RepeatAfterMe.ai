from transformers import pipeline
import difflib

class PronunciationEvaluator:
    def __init__(self):
        self.asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")
    
    def transcribe(self, audio):
        result = self.asr(audio)
        return result['text'].lower().strip()

    def get_score(self, target_text, transcribed_text):
        similarity = difflib.SequenceMatcher(None, target_text, transcribed_text)
        return similarity.ratio()
    
    def evaluate(self, audio, target_text):
        transcription = self.transcribe(audio)
        score = self.get_score(target_text.lower(), transcription)
        return {
            "transcription": transcription,
            "score": round(score, 3)  
        }
        
if __name__ == "__main__":
    evaluator = PronunciationEvaluator()
    file_audio = "banana.wav"
    target_word = "banana"
    result = evaluator.evaluate(file_audio, target_word)
    print("Transcribed:", result["transcription"])
    print("Pronunciation score:", result["score"])