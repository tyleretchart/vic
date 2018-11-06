import requests


# code = "import RPi.GPIO as GPIO\nGPIO.setmode(GPIO.BCM)\nGPIO.output(18, GPIO.HIGH)"
# code = "led = LED(18)\nled.on()"
# code = "led = LED(18)\nled.on()\nled.off()"
code = "led = LED(18)\nled.on()\ntime.sleep(1)\nled.off()"
# code = "x = 5; print(x)"
print(code)
r = requests.post(url='http://elderberry:8000/start', data={"code": code})