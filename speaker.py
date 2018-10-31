import pyttsx3

class Speaker:

    def __init__(self, out_loud):
        self.out_loud = out_loud
        if self.out_loud:
            self.engine = pyttsx3.init()

    def speak(self, string):
        self.__say(string)
        print(string)

    def prompt(self, string):
        self.__say(string)
        return input(string)

    def __say(self, string):
        if self.out_loud:
            self.engine.say(string)
            self.engine.runAndWait()