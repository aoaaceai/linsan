#!/bin/python -i
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import pickle

RATE = 44100

def dump(obj, filename):
    pickle.dump(obj, open(filename, 'bw'))

def load(filename):
    return pickle.load(open(filename, 'br'))

def argmax(arr):
    best_loc, best_abs = 0, -1
    for idx, cur in enumerate(arr):
        cur_abs = abs(cur)
        if cur_abs > best_abs:
            best_loc, best_abs = idx, cur_abs
    return best_loc

def complex_max(arr):
    return arr[argmax(arr)]

def complex_lt(a, b):
    return abs(a) < abs(b)

def get_base(trans):
    begin = int(90 * len(trans) * 2 / RATE)
    end = int(300 * len(trans)  * 2 / RATE)
    return argmax(trans[begin:end]) + begin

feature = [1.        , 0.31326637, 0.17808234, 0.04167538, 0.06481994,
       0.11314034, 0.13422605, 0.27359152]
def alxify(trans):
    r = trans[:]
    base = get_base(r)
    print(f'{base=}')
    for i in range(1, 7):
        for j in range(-2, +3):
            r[(base+j) * i] = r[base+j] * feature[i-1]
    return r

def pitch_shift(trans, shift):
    assert shift <= 1
    r = np.zeros_like(trans)
    for i in range(len(trans)):
        x = shift * i
        a = int(np.floor(x))
        t = a + 1 - x
        r[a] += trans[i] * t
        r[a+1] += trans[i] * (1-t)
    return r

def transform(sound):
    trans = fft.rfft(sound)
    print(f'{get_base(trans)=}')
    trans = alxify(trans)
    trans = pitch_shift(trans, 0.87)
    rev = fft.irfft(trans)
    return rev

if __name__ == '__main__':
    left = load('aoa')
    assert len(left.shape) == 1

    rev = transform(left)
    dump(rev, 'aoa.alx')
