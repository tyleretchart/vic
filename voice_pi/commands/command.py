import copy

class Command:
    def __init__(self, command=None):
        self.TAB = "    "
        if command is None:
            self.imports = "import time\nfrom gpiozero import LED\n\n"
            self.header = "led = LED(PIN_NUMBER)\n"
            self.code_lines = []
            self.human_lines = []
        else:
            self.imports = copy.deepcopy(command.imports)
            self.header = copy.deepcopy(command.header)
            self.code_lines = copy.deepcopy(command.code_lines)
            self.human_lines = copy.deepcopy(command.human_lines)

    def export_code(self, pin_number, include_imports=False):
        if include_imports:
            code = self.imports
        else:
            code = ""
        code += self.header
        code = code.replace("PIN_NUMBER", str(pin_number))
        tab = ""
        for line in self.code_lines:
            if line.startswith("START REPEAT: "):
                if line.endswith("forever"):
                    code += tab + "while True:\n"
                else:
                    code += tab + "for _ in range({}):\n".format(line[14:])
                tab += self.TAB
            elif line.startswith("END REPEAT"):
                tab = tab[len(self.TAB):]
            else:
                code += tab + line + "\n"
        return code

    def get_human_lines(self):
        pass

    def add_pass(self):
        self.code_lines.append("pass")
    
    def add_turn_on(self):
        self.code_lines.append("led.on()")

    def add_turn_off(self):
        self.code_lines.append("led.off()")

    def add_sleep(self, how_long):
        if how_long == "forever":
            how_long = "-1"
        self.code_lines.append("time.sleep({})".format(how_long))

    def add_command(self, command):
        self.code_lines.extend(command.code_lines)
        self.human_lines.extend(command.human_lines)

    def start_repeat(self, how_long):
        self.code_lines.append("START REPEAT: {}".format(how_long))

    def end_repeat(self):
        self.code_lines.append("END REPEAT")