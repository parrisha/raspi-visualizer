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
      #The stream was setup in NONBLOCKING mode, so if not data is ready yet the read will return 0
      # Don't attempt to unpack zero-length data, instead sleep briefly to wait for more data
      if l > 0:
         temp = unpack("%dh"%(len(temp)/2),temp)
         temp = np.array(temp, dtype='h')
         data = np.append(data, temp).astype('i2') 
         amount_read += l
      else:
         time.sleep(0.0001)

   #We may have read more than "chunk" amount of data, truncate the return array to only the samples that will be processed
   # If too much data was read, this will drop samples, but a perfect recreation of the input stream is not required to display
   # the audio spectrum.
   return data[0:chunk]

#Moved from main.py, still need to fully test
def read_wavfile(chunk, input, output):
      # Before processing samples in FFT, write raw data to speakers
      output.write(data)
      # Replace the %d in the format string with length of data chunk.
      #  Will not error if fewer than chunk samples are read at end of file
      data = unpack("%dh"%(len(data)/2),data)
      data = np.array(data, dtype='h')
