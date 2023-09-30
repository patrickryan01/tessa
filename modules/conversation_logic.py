from flask import Flask, jsonify, request
import requests, os, redis, openai
from Crypto.Cipher import AES
import base64
import requests
from gtts import gTTS
import speech_recognition as sr

app = Flask(__name__)

# Initialize OpenAI and Redis
openai.api_key = "YOUR_OPENAI_API_KEY"
r = redis.Redis(host='localhost', port=6379, db=0)

#Smart Lock API
LOCK_API_URL = "https://example.com/lock"

# Encryption setup
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
SECRET_KEY = os.urandom(32)

def encrypt(raw, key):
    raw = pad(raw)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))



@app.route("/converse", methods=["POST"])
def converse():
    user_input = request.json.get("query", "")
    
    # Convert speech to text
    if request.json.get("audio"):
        user_input = convert_speech_to_text(request.json.get("audio"))
    
    # Get user context from Redis
    user_context = r.get(f"user_{request.remote_addr}")
    
    # OpenAI API call
    response = openai.Completion.create(
      model="gpt-4.0-turbo",
      prompt=user_input,
      max_tokens=150,
      n=1,
      stop=None,
      temperature=0.7
    )
    
    reply = response.choices[0].text.strip()
    
    # Store new context
    r.set(f"user_{request.remote_addr}", user_context)
    
    # Convert text to speech
    audio_reply = convert_text_to_speech(reply)
    
    return jsonify({"response": reply, "audio": audio_reply})

def convert_text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    with open("response.mp3", "rb") as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
    return encoded_audio

def convert_speech_to_text(audio_data):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "Could not request results; {0}".format(e)

if __name__ == "__main__":
    app.run(ssl_context=("path_to_cert.pem", "path_to_key.pem"))