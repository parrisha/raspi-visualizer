import alsaaudio as aa
import wave
import numpy as np
from struct import unpack
import time
import argparse

from spectrum import spectrum
from led import Matrix16x8

#Will only be executed if this file is called directly from python
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Read samples from a .wav file and display Audio spectrum on LEDs')
   parser.add_argument('wavfile', type=argparse.FileType('rb'))
   parser.add_argument('--scale', type=int, default=4)
   parser.add_argument('--use_mic', action='store_true')
   args = parser.parse_args()

   chunk = 4096
   num_columns = 16

   if (args.use_mic == True):
      #Setup an AlsaAudio stream to read data from microphone
      # Already configured using alsamixer and alsarecord
      input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK, cardindex=1)
      input.setchannels(1)
      input.setrate(44100)
      input.setformat(aa.PCM_FORMAT_S16_LE)
      input.setperiodsize(chunk)
      #Needed to use a lambda for wave readframes() (see below)
      # So also use one here so the calls will have the same syntax
      read_data_func = lambda x,y: x.read()
   else:
      #Setup for reading from a .wav file on disk
      input = wave.open(args.wavfile)
      #The alsaaudio input object returns two values in NON_BLOCKING_MODE
      # Use a lambda function to coerce the wave readframes() function to return the same type
      read_data_func = lambda x,y: {1, x.readframes(y)}
      sample_rate = input.getframerate()
      print("Input File Sample Rate ", sample_rate)
      #Also setup to play the .wav file through the Raspberry pi audio output
      output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NONBLOCK)
      output.setchannels(1)
      output.setperiodsize(chunk)

   #Setup the LED display for writing outputs
   display = Matrix16x8.Matrix16x8()
   display.begin()
   display.clear()
   display.set_brightness(1)
   display.write_display()

   bin_mapping = spectrum.find_bin_mapping_np(num_columns, chunk, sample_rate)
   #Selected Bin Mapping:  [2, 3, 4, 7, 10, 16, 25, 38, 59, 90, 139, 215, 330, 509, 783, 1206, 1858]
   print("Selected Bin Mapping: ", bin_mapping)

   #Call the function pointer that will either read from mic or file on disk
   l, data = read_data_func(input, chunk)

   # Loop through the wave file
   while data != '':
      # Before processing samples in FFT, write raw data to speakers
      output.write(data)
      # Replace the %d in the format string with length of data chunk.
      #  Will not error if fewer than chunk samples are read at end of file
      data = unpack("%dh"%(len(data)/2),data)
      data = np.array(data, dtype='h')

      # Optional scale factor is applied to output of FFT
      #  4 is default for full scale 16-bit audio, increase if volume is really low
      bin_powers = spectrum.get_spectrum(data, bin_mapping, chunk, args.scale)
      print(bin_powers)
      np.clip(bin_powers,0,8,bin_powers)
      for col in range(0,num_columns):
         display.set_column(col, bin_powers[col])
      display.write_display()
      l, data = read_data_func(input, chunk)
      time.sleep(chunk/sample_rate)
