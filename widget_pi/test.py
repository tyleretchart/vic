import requests


r = requests.post(url='http://0.0.0.0:8000/start', data={"code": "x = 5; print(x)"})