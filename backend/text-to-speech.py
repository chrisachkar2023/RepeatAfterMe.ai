from gtts import gTTS

text = "Hello! This is a test using gTTS with an Indian English accent."

tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
tts.save("output_audio.mp3")

print("Audio saved successfully.")
