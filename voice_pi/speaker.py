import pyttsx3
from record import record_voice

class Speaker:

    def __init__(self, out_loud, listen):
        self.out_loud = out_loud
        self.listen = listen
        if self.out_loud:
            self.engine = pyttsx3.init()

    def speak(self, string):
        self.__say(string)
        print(string)

    def prompt(self, string):
        self.__say(string)
        if self.listen:
            print(string)
            msg = record_voice()
            print("You said:", msg)
            return msg
        else:
            return input(string)

    def __say(self, string):
        if self.out_loud:
            self.engine.say(string)
            self.engine.runAndWait()
