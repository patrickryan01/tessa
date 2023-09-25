import os
import shutil
import smtplib
import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

# AES Encryption setup
key = get_random_bytes(32)  # AES256 requires a 32-byte key
cipher = AES.new(key, AES.MODE_EAX)

def backup_files(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(backup_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

def send_email(subject, body, to_email):
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()  # Start TLS encryption for the connection
        server.login(decrypt(encrypted_email, email_nonce), decrypt(encrypted_password, password_nonce))
        server.sendmail("your_email@example.com", to_email, f"Subject: {subject}\n\n{body}")

def get_weather(city):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={decrypt(encrypted_api_key, api_key_nonce)}')
    data = response.json()
    return data['weather'][0]['description']

def encrypt(plain_text):
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())
    return b64encode(ciphertext).decode('utf-8'), b64encode(nonce).decode('utf-8')

def decrypt(ciphertext, nonce):
    cipher_dec = AES.new(key, AES.MODE_EAX, nonce=b64decode(nonce.encode()))
    return cipher_dec.decrypt(b64decode(ciphertext.encode())).decode('utf-8')

if __name__ == "__main__":
    # Assuming email, password, and API key were encrypted and stored earlier
    encrypted_email, email_nonce = encrypt("your_email@example.com")
    encrypted_password, password_nonce = encrypt("your_password")
    encrypted_api_key, api_key_nonce = encrypt("YOUR_API_KEY")

    # Backup files
    backup_files("/path/to/source", "/path/to/backup")

    # Send an email with decrypted credentials
    send_email("Automated Email", "This is an automated email.", "receiver@example.com")

    # Fetch and print weather data with decrypted API key
    weather = get_weather("New York")
    print(f"The weather in New York is {weather}.")