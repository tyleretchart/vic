from commands.command import Command 

class CommandBuilder:
    def __init__(self, speaker):
        self.speaker = speaker
        self.commands = {}

    def build_command(self):
        # init
        response = self.speaker.prompt("Would you like to build a command from scratch or start from an old one?\n> ")
        old_command = None
        if response == "old":
            response = self.speaker.prompt("Which command?\n> ")
            try:
                old_command = self.commands[response]
                self.speaker.speak("Success!")
            except Exception as e:
                self.speaker.speak("Sorry, {} is not a current command. Building one from scratch instead.".format(response))
        new_command = Command(old_command)

        # choose name
        name_not_chosen = True
        while name_not_chosen:
            command_name = self.speaker.prompt("Would you like to name the new command?\n> ")
            if command_name in self.commands:
                confirmation = self.speaker.prompt("That name is taken. Overwrite old command?\n> ")
                if confirmation == "yes":
                    self.speaker.speak("Ok! Overwriting {} with new command.".format(command_name))
                    name_not_chosen = False
                else:
                    self.speaker.speak("{} was not chosen as new name.".format(command_name))
            else:
                self.speaker.speak("Ok! {} is the name of the new command.".format(command_name))
                name_not_chosen = False

        # build command
        self.speaker.speak("We are going to start building the command. Say finished when you want to stop.")
        not_finished = True
        while not_finished:
            response = self.speaker.prompt("Next line:\n> ")
            if response == "pass":
                new_command.add_pass()
            elif response == "turn on":
                new_command.add_turn_on()
            elif response == "turn off":
                new_command.add_turn_off()
            elif response == "sleep":
                how_long = self.speaker.prompt("For how long?\n> ")
                new_command.add_sleep(how_long)
            elif response == "start repeat":
                how_long = self.speaker.prompt("For how long?\n> ")
                new_command.start_repeat(how_long)
            elif response == "end repeat":
                new_command.end_repeat()
            elif response == "finished":
                not_finished = False
            else:
                try:
                    defined_command = self.commands[response]
                    new_command.add_command(defined_command)
                except Exception as e:
                    self.speaker.speak("Sorry, not a valid command... try again!")

        # save command
        self.speaker.speak("Done building command!")
        self.speaker.speak("Here is your command!\n---------------------------")
        self.speaker.speak(new_command.export_code("18"))
        self.commands[command_name] = new_command
