from flask import Flask, jsonify, request
import requests
from Crypto.Cipher import AES
import base64
import os

app = Flask(__name__)

# Smart device API endpoints (replace with actual endpoints)
LIGHT_API_URL = "http://lighting.local/api"
THERMOSTAT_API_URL = "http://thermostat.local/api"

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

SECRET_KEY = os.urandom(32)

@app.route("/lights/on", methods=["POST"])
def lights_on():
    # Example call to smart lighting system API
    response = requests.post(f"{LIGHT_API_URL}/on")
    
    if response.status_code == 200:
        encrypted_data = encrypt(response.text, SECRET_KEY)
        return jsonify({"data": encrypted_data.decode('utf-8')})
    else:
        return jsonify({"error": "Failed to turn on lights."}), 400

@app.route("/lights/off", methods=["POST"])
def lights_off():
    response = requests.post(f"{LIGHT_API_URL}/off")
    
    if response.status_code == 200:
        encrypted_data = encrypt(response.text, SECRET_KEY)
        return jsonify({"data": encrypted_data.decode('utf-8')})
    else:
        return jsonify({"error": "Failed to turn off lights."}), 400

@app.route("/thermostat/set_temp", methods=["POST"])
def set_temperature():
    temp = request.json.get("temperature")
    
    response = requests.post(f"{THERMOSTAT_API_URL}/set", json={"temp": temp})
    
    if response.status_code == 200:
        encrypted_data = encrypt(response.text, SECRET_KEY)
        return jsonify({"data": encrypted_data.decode('utf-8')})
    else:
        return jsonify({"error": "Failed to set temperature."}), 400
    
@app.route("/lock", methods=["POST"])
def lock():    
    # Example call to smart lock system API
    response = requests.post(f"{LOCK_API_URL}/lock")
    
    if response.status_code == 200:
        encrypted_data = encrypt(response.text, SECRET_KEY)
    
    
if __name__ == "__main__":
    app.run(ssl_context=("path_to_cert.pem", "path_to_key.pem"))