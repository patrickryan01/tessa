import speech_recognition as sr

class TESSA:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def listen(self):
        """
        Listen for commands using the microphone and return the recognized text.
        """
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
                return None

