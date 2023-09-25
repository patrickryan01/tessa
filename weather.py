from flask import Flask, jsonify, request
import requests
from Crypto.Cipher import AES
import base64
import os

app = Flask(__name__)

OPEN_WEATHER_API_KEY = "YOUR_OPEN_WEATHER_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Encryption setup
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

def encrypt(raw, key):
    raw = pad(raw)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, key):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(enc[AES.block_size:]).rstrip(b"\0")

SECRET_KEY = os.urandom(32)  # This generates a new key on each run. Store securely if persistent key needed.

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", default="Los Angeles,USA")
    response = requests.get(BASE_URL, params={
        "q": city,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric"  # Using metric units
    })

    if response.status_code == 200:
        encrypted_data = encrypt(response.text, SECRET_KEY)
        return jsonify({"data": encrypted_data.decode('utf-8')})
    else:
        return jsonify({"error": "Could not retrieve weather data."}), 400

@app.route("/decrypt", methods=["POST"])
def decrypt_data():
    encrypted_data = request.json.get("data")
    if not encrypted_data:
        return jsonify({"error": "Missing data."}), 400

    decrypted_data = decrypt(encrypted_data.encode('utf-8'), SECRET_KEY)
    return jsonify({"data": decrypted_data.decode('utf-8')})

if __name__ == "__main__":
    app.run(ssl_context=("path_to_cert.pem", "path_to_key.pem"))