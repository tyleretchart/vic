import intents
import requests
import subprocess
from widgets.widget import Widget

class WidgetRegistrar:
    def __init__(self):
        self.widgets = {}

    def scan(self):
        # scan for ips on the local network
        hostnames = {}
        try:
            nmap_result = subprocess.check_output("nmap -sP 192.168.1.1/24", shell=True).decode().strip().split("\n")
            for result in nmap_result:
                hostname, ip = intents.get_hostnames(result)
                if hostname is not None:
                    hostnames[hostname] = ip
        except Exception as e:
            print("ERROR", e)

        # remove any known widgets
        # for known in self.widgets.keys():
        #     if known in hostnames:
        #         del hostnames[known]
        return hostnames

    def rebuild_network(self, hostnames):
        self.widgets = {}
        for name, ip in hostnames.items():
            try:
                r = requests.post(url='http://{}:8000/widget'.format(self.ip))
                if r.text == "True":
                    self.widgets[hostname] = Widget(name=hostname, ip=ip)
            except Exception as e:
                pass


    def add_widget(self, hostname, ip):
        self.widgets[hostname] = Widget(name=hostname, ip=ip)