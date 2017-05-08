####################
# George Mason University - ECE612
# Aaron Joe Parrish - Spring 2017
#
# Final Project
#  mic.py
#  Uses alsaaudio to read samples from a USB micrphone 
####################
import numpy as np
import alsaaudio as aa
from struct import unpack
import time

# Will read small read_size packets from the mic and append until "chunk" data has been read
def read_mic(chunk, input):
   # Create an empty NumPy array that will store the mic data
   data = np.array([])
   amount_read = 0

   while amount_read <= chunk:
      l, temp = input.read()
      if l > 0:
         temp = unpack("%dh"%(len(temp)/2),temp)
         temp = np.array(temp, dtype='h')
         data = np.append(data, temp).astype('i2') 
         amount_read += l
      else:
         time.sleep(0.0001)

   return data[0:chunk]

#Moved from main.py, still need to fully test
def read_wavfile(chunk, input, output):
      # Before processing samples in FFT, write raw data to speakers
      output.write(data)
      # Replace the %d in the format string with length of data chunk.
      #  Will not error if fewer than chunk samples are read at end of file
      data = unpack("%dh"%(len(data)/2),data)
      data = np.array(data, dtype='h')
