import wave
import pyaudio
import requests
from serializer import Serializer
from gpiozero import Button, LED

def record_voice(self):
    # globals
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3
    button = Button(27)
    led = LED(18)

    # start recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    # print("recording...")
    frames = []

    # record for RECORD_SECONDS
    button.wait_for_press()
    led.on()
    while button.is_pressed:
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    led.off()
    # print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # write your new .wav file with built in Python 3 Wave module
    waveFile = wave.open("out.wav", 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # stt
    s = Serializer()
    with open("out.wav", "rb") as fin:
        r = requests.post(url="http://192.168.1.172:8000/transcribe", data={"audio": s.serialize(fin.read())})
    print(r.json())
    return r.json()["msg"]
