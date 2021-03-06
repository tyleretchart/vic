import sys
import readline

from pprint import pprint

import intents
from speaker import Speaker
from commands import CommandBuilder
from widgets import WidgetRegistrar

speaker = Speaker(out_loud=True, listen=True)
command_builder = CommandBuilder(speaker=speaker)
wregistrar = WidgetRegistrar()


def main():
    speaker.speak("Hello, my name is VIC!")
    while True:
        response = speaker.prompt("What would you like to do now?\n> ")

        # scan for new widgets
        if intents.scan_new_widgets(response):
            hostnames = wregistrar.scan()
            print(hostnames)
            wregistrar.rebuild_network(hostnames)
            if wregistrar.widgets:
                speaker.speak("We have scanned your network and found these widgets")
                for hostname in wregistrar.widgets.keys():
                    speaker.speak(hostname)
            else:
                speaker.speak("Sorry, there are no widgets on the network.")

        # ask to hear current widgets
        elif intents.share_current_widgets(response):
            number_display = "Sure! You have {} widget".format(
                len(wregistrar.widgets))
            if len(wregistrar.widgets) == 1:
                number_display += "."
            else:
                number_display += "s."
            speaker.speak(number_display)
            for name, data in wregistrar.widgets.items():
                if len(data["lights"]) > 0:
                    speaker.speak("{} widget has registered lights {}".format(
                        name, " ".join(data["lights"])))
                else:
                    speaker.speak(
                        "{} widget has no registered lights yet".format(name))

        # build new command
        elif intents.build_new_command(response):
            command_builder.build_command()

        # send command
        elif intents.send_command(response):
            response = speaker.prompt("Which command?\n> ")
            try:
                command = command_builder.commands[response]
            except Exception as e:
                speaker.speak("Sorry, that isn't a valid command.")
                continue

            response = speaker.prompt("Which widget?\n> ")
            try:
                widget = wregistrar.widgets[response]
            except Exception as e:
                speaker.speak("Sorry, that isn't a valid widget.")
                continue
            
            response = speaker.prompt("Which pin?\n> ")
            try:
                pin = int(response)
            except Exception as e:
                speaker.speak("Sorry, that isn't a valid pin.")
                continue
            response = widget.send_command(command, pin)
            speaker.speak(response)

        # random phrase to show off voice
        elif intents.party(response):
            speaker.speak("It's party time!")

        else:
            speaker.speak(
                "I didn't understand your command, please try again!\n")


if __name__ == "__main__":
    sys.exit(main())
