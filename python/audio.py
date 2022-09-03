#!/bin/python -i
import sounddevice as sd
import numpy as np

RATE = 44100

sd.default.samplerate = RATE
sd.default.channels = 2
# sd.default.device = ''

duration = 1

from time import sleep

def record():
    recording = sd.rec(int(RATE * duration), blocking=True)
    recording *= 10
    left = recording[:, 0]
    return left

def playback(recording):
    sd.play(recording, blocking=True)


record()
record()
print('begin in a second')
sleep(1)

left = record()
print('done')
playback(left)
import pickle
pickle.dump(left, open('alx', 'bw'))
