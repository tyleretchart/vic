from commands.command import Command
from commands.command_builder import CommandBuilder

# command = Command()

# command.add_turn_on()
# command.add_turn_off()
# command.start_repeat("20")
# command.add_sleep("20")
# command.end_repeat()
# command.start_repeat("forever")
# command.add_pass()
# command.end_repeat()

# command2 = Command(command)
# command2.add_turn_on()

# print(command.export_code(18))
# print("-----------")
# print(command2.export_code(18))

cb = CommandBuilder()

cb.build_command()