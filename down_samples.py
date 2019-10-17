#!usr/bin/env python
# coding=utf-8
import numpy as np


import pyaudio
import wave

# Returns a byte-scaled image
def bytescale(data, dtype=np.int16, factor = 32):


    scale = 1 / float(factor)
    bytedata = data * scale - 0.1
    print(bytedata.dtype)
    bytedata = np.cast[dtype](bytedata) * factor

    sum = np.cast[dtype](bytedata)
    return sum.__add__(data)
    return data



# define stream chunk
chunk = 1024

# open a wav format music
f = wave.open(r"Bassline.wav", "rb")
# instantiate PyAudio
p = pyaudio.PyAudio()
# open stream
print(p.get_format_from_width(f.getsampwidth()))
stream = p.open(format=p.get_format_from_width(2),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True)


def chunk_stream():
    while True:
        yield f.readframes(chunk)
    # yield None


def crush(samp, dtype=np.int8):
    np_arr = np.frombuffer(samp, dtype=dtype)
    # np_arr = np.fromstring(samp, dtype='>u4')
    print(np_arr.dtype)
    try:
        np_arr = bytescale(np_arr, dtype=dtype)
    except ValueError as err:  # raised if `y` is empty.
        print(err)

    return np_arr.astype(dtype, 'F')


# read data
for data in chunk_stream():
    print(len(data))
    new = crush(data)
    print(len(data))
    stream.write(new)

# stop stream
stream.stop_stream()
stream.close()

# close PyAudio
p.terminate()
