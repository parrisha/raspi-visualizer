import alsaaudio as aa
import wave
import numpy as np
from struct import unpack
import time

from spectrum import spectrum


#Will only be executed if this file is called directly from python
if __name__ == '__main__':
   chunk = 4096
   wavfile = wave.open('/home/pi/ECE_612/samples/glass_animals.wav')

   sample_rate = wavfile.getframerate()
   print("Input File Sample Rate ", sample_rate)

   output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
   output.setchannels(1)
   output.setperiodsize(chunk)

   bin_mapping = find_bin_mapping_np(16, chunk, sample_rate)
   bin_weights = find_bin_weights_np(16, chunk)
   #Selected Bin Mapping:  [2, 3, 4, 7, 10, 16, 25, 38, 59, 90, 139, 215, 330, 509, 783, 1206, 1858]
   print("Selected Bin Mapping: ", bin_mapping)

   data = wavfile.readframes(chunk)

   # Loop through the wave file
   while data != '':
      # Replace the %d in the format string with length of data chunk.
      #  Will not error if fewer than chunk samples are read at end of file
      data = unpack("%dh"%(len(data)/2),data)
      data = np.array(data, dtype='h')

      bin_powers = get_spectrum(data, bin_mapping, chunk, sample_rate)
      # Bin powers are very large numbers!  Need to scale down to fit on the 8-height array
      bin_powers = np.divide(bin_powers,1000000000)
      bin_powers = np.round(bin_powers)
      print(bin_powers)
      data = wavfile.readframes(chunk)
      time.sleep(1)

