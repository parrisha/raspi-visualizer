import alsaaudio as aa
import wave
import numpy as np
from struct import unpack
import time

from spectrum import spectrum
from led import Matrix16x8

#Will only be executed if this file is called directly from python
if __name__ == '__main__':
   chunk = 4096

   #Setup for reading from a .wav file on disk
   wavfile = wave.open('/home/pi/ECE_612/samples/glass_animals.wav')
   sample_rate = wavfile.getframerate()
   print("Input File Sample Rate ", sample_rate)
   output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
   output.setchannels(1)
   output.setperiodsize(chunk)

   #Setup the LED display for writing outputs
   display = Matrix16x8.Matrix16x8()
   display.begin()
   display.clear()
   display.set_brightness(1)
   display.write_display()

   bin_mapping = spectrum.find_bin_mapping_np(16, chunk, sample_rate)
   #Selected Bin Mapping:  [2, 3, 4, 7, 10, 16, 25, 38, 59, 90, 139, 215, 330, 509, 783, 1206, 1858]
   print("Selected Bin Mapping: ", bin_mapping)

   data = wavfile.readframes(chunk)

   # Loop through the wave file
   while data != '':
      # Replace the %d in the format string with length of data chunk.
      #  Will not error if fewer than chunk samples are read at end of file
      data = unpack("%dh"%(len(data)/2),data)
      data = np.array(data, dtype='h')

      # Optional scale factor is applied to output of FFT
      #  4 is default for full scale 16-bit audio, increase if volume is really low
      bin_powers = spectrum.get_spectrum(data, bin_mapping, chunk, scale=9)
      print(bin_powers)
      for col in range(0,8):
         display.set_column(col, bin_powers[col])
      display.write_display()
      data = wavfile.readframes(chunk)
      time.sleep(1)
