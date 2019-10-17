import numpy as np
import cv2
import soundcard as sc  # Get it from https://github.com/bastibe/SoundCard
import collections

imWidth, imHeight = 1024, 512  # screen size

buff = collections.deque([0.0] * 10, maxlen=10)


def draw_wave(screen, mono_audio, xs, title="oscilloscope", gain=3, print_avg=False):
    # freq = find_freq(mono_audio[0:len(xs)], len(xs))
    peak_volume = np.max(mono_audio[0:len(xs)])
    buff.append(peak_volume)
    avg = np.mean(buff)
    weight = peak_volume + avg / 3.0

    # flash background
    cv2.addWeighted(screen, 1 - weight, np.full((imHeight, imWidth, 3), [200, 200, 255], dtype=np.uint8), weight, 1,
                    screen)

    # fade out image (multiply would be preferred but turns everything blue)
    # cv2.multiply(screen, 0.66, screen)
    cv2.addWeighted(screen, .8, np.zeros((imHeight, imWidth, 3), dtype=np.uint8), 0.2, 0, screen)

    ys = imHeight / 2 * (1 - np.clip(gain * mono_audio[0:len(xs)], -1, 1))  # the y-values of the waveform
    pts = np.array(list(zip(xs, ys))).astype(np.int)  # pair up xs & ys
    cv2.polylines(screen, [pts], False, (200, 100, 255), thickness=18)  # connect points w/ lines
    cv2.polylines(screen, [pts], False, (100, 50, 255), thickness=12)  # connect points w/ lines
    cv2.polylines(screen, [pts], False, (0, 0, 255), thickness=4)

    if print_avg:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(screen, str(avg), (10, 500), font, 4, (255, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow(title, screen)  # show what we've got
    return screen


def find_volume(np_arr, frate):
    w = np.fft.fft(np_arr)
    freqs = np.fft.fftfreq(len(w))
    print(freqs.min(), freqs.max())
    # (-0.5, 0.499975)

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * frate)
    return freq_in_hertz


default_mic = sc.default_microphone()
screen = np.zeros((imHeight, imWidth, 3), dtype=np.uint8)  # 3=color channels
xs = np.arange(imWidth).astype(np.int)  # x values of pixels
while (1):  # keep looping until someone stops this madness
    with default_mic.recorder(samplerate=44100) as mic:
        audio_data = mic.record(numframes=1024)  # get some audio from the mic
    screen = draw_wave(screen, audio_data[:, 0], xs)  # draw left channel
    key = cv2.waitKey(1) & 0xFF  # keyboard input
    if ord('q') == key:  # quit key
        break
