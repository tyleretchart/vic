from commands.command import Command 

class CommandBuilder:
    def __init__(self):
        self.commands = {}

    def build_command(self):
        response = input("Would you like to build a command from scratch or start from an old one?\n> ")
        if response == "new":
            new_command = Command()
        else:
            new_command = Command()

        print("Ok, we are going to start building the command. Say finished when you want to stop.")
        not_finished = True
        while not_finished:
            response = input("Next line:\n> ")
            if response == "pass":
                new_command.add_pass()
            elif response == "turn on":
                new_command.add_turn_on()
            elif response == "turn off":
                new_command.add_turn_off()
            elif response == "turn off":
                new_command.add_turn_off()
            elif response == "sleep":
                how_long = input("For how long?\n> ")
                new_command.add_sleep(how_long)
            elif response == "start repeat":
                how_long = input("For how long?\n> ")
                new_command.start_repeat(how_long)
            elif response == "end repeat":
                new_command.end_repeat()
            elif response == "finished":
                not_finished = False
            else:
                print("Sorry, not a valid command... try again!")
        print("Here is your command!\n---------------------------")
        print(new_command.export_code("18"))