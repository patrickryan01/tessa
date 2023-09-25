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

    def process_command(self, command):
        """
        Process the given command and execute the appropriate action.
        """
        # For simplicity, we'll just print the command now. Later, you'll add actual actions.
        if command:
            print(f"You said: {command}")

    def wake_word_detected(self, command):
        """
        Check if the wake word (e.g., "Hey TESSA") is present in the command.
        """
        return "hey tessa" in command.lower()

    def run(self):
        """
        Main loop to keep TESSA running and listening for the wake word.
        """
        while True:
            command = self.listen()
            if command and self.wake_word_detected(command):
                print("Activated! What can I do for you?")
                command = self.listen()
                self.process_command(command)

if __name__ == "__main__":
    tessa = TESSA()
    tessa.run()