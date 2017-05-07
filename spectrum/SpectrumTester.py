####################
# George Mason University - ECE612
# Aaron Joe Parrish - Spring 2017
#
# Final Project
#  SpectrumTester.py
#  Test the Bin-Mapping and FFT/Scaling functions by generating and injecting sinusoids
#  and graphing the result as a MatPlotLib bar graph
#  The Raspberry PI does not have MatPlotLib or a display, so only intended to run on a test machine
####################
import matplotlib.pyplot as plt
import numpy as np
import time
from . import spectrum


##TEST##
#Use numpy to generate a single frame of sine waves to feed into the FFT
# Each wave can have a configurable frequency and amplitude
# The data is cast to int16, so a total amplitude over 32767 may saturate
#Then use matplotlib to graph the PSD output
#
# test_freqs: An array of integers representing frequencies in Hz to generate sine waves
# test_amps:  An array of integers representing at what amplitude to generate each sine wave from test_freqs
# chunk:      The data length and FFT size, defaults to 4096
# samplerate: Samplerate used to generate sine waves.  Defaults to rate of audio CDs, 44.1 KHz
def spectrum_test(test_freqs, test_amps, scale=12, chunk=4096, samplerate=44100):
    num_columns = 16
    
    x = np.arange(chunk)
    y = np.zeros(chunk)
    for test_freq,test_amp in zip(test_freqs,test_amps):
       y = np.add(y, np.sin(2 * np.pi * test_freq * x / samplerate) * test_amp)

    #Cast to int16 - the data format returned by the microphone
    y = y.astype('i2')   

    bin_powers = spectrum.get_spectrum(y, spectrum.find_bin_mapping_np(num_columns), chunk, scale)

    plt.bar(np.arange(num_columns), spectrum, 1, align='edge')
    plt.show()
    
