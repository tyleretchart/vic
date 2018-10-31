import requests


r = requests.post(url='http://0.0.0.0:8000/start', data={"code": "while True: pass"})