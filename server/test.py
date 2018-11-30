import wave
import requests

import _pickle as pickle 

class Serializer:

    def __init__(self):
        pass

    def serialize(self, generic_object):
        byte_str = pickle.dumps(generic_object)
        return byte_str.hex()

    def deserialize(self, object_string):
        object_string = bytes.fromhex(object_string)
        return pickle.loads(object_string)

s = Serializer()

with open("test.wav", 'rb') as fin:
    r = requests.post(url='http://localhost:8000/transcribe', data={"audio": s.serialize(fin.read())})
print(r.json())
