from pprint import pprint
import readline

import intents
from registrar import Registrar
from speaker import Speaker

registrar = Registrar()
speaker = Speaker(out_loud=False)

speaker.speak("Hello, my name is VIC!")
while True:
    response = speaker.prompt("What would you like to do now?\n> ")

    # scan for new widgets
    if intents.scan_new_widgets(response):
        hostnames = registrar.scan()
        widget_not_found = True
        for name, ip in hostnames.items():
            response = speaker.prompt("Is {} the widget you are looking for?\n> ".format(name))
            if intents.yes(response):
                registrar.add_widget(name, ip)
                speaker.speak("Great! {} has been registered\n".format(name))
                widget_not_found = False
                break
        if widget_not_found:
            speaker.speak("Sorry, we couldn't find your widget...\n")

    # ask to hear current widgets
    elif intents.share_current_widgets(response):
        number_display = "Sure! You have {} widget".format(len(registrar.widgets))
        if len(registrar.widgets) == 1:
            number_display += "."
        else:
            number_display += "s."
        speaker.speak(number_display)
        for name, data in registrar.widgets.items():
            if len(data["lights"]) > 0:
                speaker.speak("{} widget has registered lights {}".format(name, " ".join(data["lights"])))
            else:
                speaker.speak("{} widget has no registered lights yet".format(name))

    else:
        speaker.speak("I didn't understand your command, please try again!\n")