#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave
import os
import sys
import signal
import psutil
import logging

from io import BytesIO, BufferedReader
from sanic import Sanic
from sanic.response import json
from multiprocessing import Process
from deepspeech import Model, printVersions
from timeit import default_timer as timer
from serializer import Serializer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

#
# -------------------------------------------------
# helpers

def convert_samplerate():
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote("tmp.wav"))
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

    return 16000, np.frombuffer(output, np.int16)


class VersionAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super(VersionAction, self).__init__(nargs=0, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        printVersions()
        exit(0)

#
# -------------------------------------------------
# globals

s = Serializer()
app = Sanic()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger()

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_WEIGHT = 1.50

# Valid word insertion weight. This is used to lessen the word insertion penalty
# when the inserted word is part of the vocabulary
VALID_WORD_COUNT_WEIGHT = 2.10

# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9

model = "models/output_graph.pbmm"
alphabet = "models/alphabet.txt"
lm = "models/lm.binary"
trie = "models/trie"

print('Loading model from file {}'.format(model), file=sys.stderr)
model_load_start = timer()
ds = Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
model_load_end = timer() - model_load_start
print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

if lm and trie:
    print('Loading language model from files {} {}'.format(lm, trie), file=sys.stderr)
    lm_load_start = timer()
    ds.enableDecoderWithLM(alphabet, lm, trie, LM_WEIGHT,
                            VALID_WORD_COUNT_WEIGHT)
    lm_load_end = timer() - lm_load_start
    print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)

#
# -------------------------------------------------
# main

@app.route('/transcribe', methods=["POST",])
async def transcribe(request):
    raw_audio = request.form.get("audio")
    raw_audio = s.deserialize(raw_audio)
    audio = BufferedReader(BytesIO(raw_audio))
    fin = wave.open(audio, 'rb')

    fout = wave.open("tmp.wav", "wb")
    fout.setnchannels(fin.getnchannels())
    fout.setsampwidth(fin.getsampwidth())
    fout.setframerate(fin.getframerate())
    fout.writeframes(raw_audio)
    fout.close()

    fs = fin.getframerate()
    if fs != 16000:
        print('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs), file=sys.stderr)
        fs, audio = convert_samplerate()
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/16000)
    fin.close()

    print('Running inference.', file=sys.stderr)
    inference_start = timer()
    words = ds.stt(audio, fs)
    print(words)
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
    return json({"error": False, "msg": words})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)