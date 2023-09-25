import speech_recognition as sr
from gtts import gTTS
import pygame

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class TESSA:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.key = get_random_bytes(32)  # AES256 requires a 32-byte key
        self.cipher = AES.new(self.key, AES.MODE_EAX)
        self.wake_words = [
            "hey tessa",
            "good morning tessa",
            "good afternoon tessa",
            "good evening tessa",
            "tessa"
        ]
        
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")  # This is for my own debug purpose
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                self.respond("Sorry, I didn't catch that.")
                return None

    def encrypt(self, plaintext):
        nonce = self.cipher.nonce
        ciphertext, tag = self.cipher.encrypt_and_digest(plaintext.encode())
        return (nonce, ciphertext)

    def decrypt(self, nonce, ciphertext):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext).decode()

    def respond(self, message):
        tts = gTTS(text=message, lang="en")
        tts.save("response.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def process_command(self, command):
        if command:
            encrypted_data = self.encrypt(command)
            decrypted_data = self.decrypt(*encrypted_data)
            self.respond(f"You said: {decrypted_data}")  # Here we respond using speaker

    def wake_word_detected(self, command):
        return any(wake_word in command.lower() for wake_word in self.wake_words)

    def run(self):
        while True:
            command = self.listen()
            if command and self.wake_word_detected(command):
                self.respond("Activated! What can I do for you?")
                command = self.listen()
                self.process_command(command)

if __name__ == "__main__":
    tessa = TESSA()
    tessa.run()
