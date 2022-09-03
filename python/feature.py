#!/bin/python -i
import numpy.fft as fft
import numpy as np
import pickle
import matplotlib.pyplot as plt

RATE = 44100

def load(filename):
    return pickle.load(open(filename, 'br'))

def filter_human(trans):
    begin = 70
    end = 5000
    # begin = int(90 * len(trans) / RATE)
    # end = int(5000 * len(trans) / RATE)
    r = np.zeros_like(trans)
    r[begin:end] = trans[begin:end]
    return r

def filter_base(trans):
    begin = 70
    end = 320
    # begin = int(90 * len(trans) / RATE)
    # end = int(320 * len(trans) / RATE)
    r = np.zeros_like(trans)
    r[begin:end] = trans[begin:end]
    return r

def argmax(arr):
    best_loc, best_abs = 0, -1
    for idx, cur in enumerate(arr):
        cur_abs = abs(cur)
        if cur_abs > best_abs:
            best_loc, best_abs = idx, cur_abs
    return best_loc

def purify(trans):
    r = trans[:]
    M = argmax(filter_base(r))
    print(f'base: {M}')
    for i in range(len(r)):
        if i % M:
            r[i] = 0
    return r

def dump(obj, filename):
    pickle.dump(obj, open(filename, 'bw'))

def feature_vector(trans):
    r = np.array([abs(i) for i in trans[70:5000] if abs(i)][:50])
    return r / r[0]

def extract_feature(filename):
    print(f'{filename=}')
    sound = load(filename)
    trans = fft.rfft(sound)
    trans = filter_human(trans)
    trans = purify(trans)
    return trans

def alxify(trans):
    r = trans[:]
    base = argmax(filter_base(r))
    print(f'{base=}')
    r[base] *= 5
    r[base * 2] = r[base] * 0.31326637
    r[base * 3] = r[base] * 0.17808234
    r[base * 4] = r[base] * 0.04167538
    r[base * 5] = r[base] * 0.06481994
    return r

pao = extract_feature('pao')
aoa = extract_feature('aoa')
aoa2 = extract_feature('aoa2')
alx = extract_feature('alx')
aoa2_vec = feature_vector(aoa2)
alx_vec = feature_vector(alx)

for vec in [aoa2_vec, alx_vec]:
    plt.plot(vec)
plt.show()

print(f'{aoa2_vec=}')
print(f'{alx_vec=}')
