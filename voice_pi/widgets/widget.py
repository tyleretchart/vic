import requests

class Widget:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.lights = {}

    def send_command(self, command, pin):
        code = command.export_code(pin, include_imports=False)
        r = requests.post(url='http://0.0.0.0:8000/start', data={"code": code})
        return r.text
