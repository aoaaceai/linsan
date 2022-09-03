#!/bin/python -i
import sounddevice as sd

RATE = 44100

sd.default.samplerate = RATE
sd.default.channels = 1

import pickle
import numpy as np

def play(filename):
    sound = pickle.load(open(filename, 'br'))
    sd.play(sound, blocking=True)

