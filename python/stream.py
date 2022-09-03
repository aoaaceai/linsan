#!/bin/python
import sounddevice as sd
from transform import transform
import numpy as np

RATE=44100
sd.default.samplerate = RATE
sd.default.channels = 1

class Buffer:
    def __init__(self, size):
        self.__container = np.zeros(size, dtype=np.float32)
        self.__size = size

    def push(self, content):
        assert len(content) <= self.__size
        r = self.__container[:len(content)]
        self.__container = np.append(self.__container[len(content):], content)
        return r

    def get(self):
        return self.__container[:]

    def __len__(self):
        return self.__size

buffer = Buffer(7350)

def func(indata, outdata, frames, time, status):
    sound = indata[:, 0]
    buffer.push(sound)
    full = buffer.get()
    full = transform(full)
    outdata[:] = full[:frames].reshape((-1, 1))

def finished():
    print('finished')

stream = sd.Stream(blocksize=7350, callback=func, finished_callback=finished)

stream.start()

from signal import pause
try:
    pause()
except:
    pass
stream.stop()
