import alsaaudio as aa
import wave
import numpy as np
from struct import unpack
import time
import argparse

from spectrum import spectrum
from mic import mic
from led import Matrix16x8

#Will only be executed if this file is called directly from python
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Read samples from a .wav file and display Audio spectrum on LEDs')
   parser.add_argument('--wavfile', type=argparse.FileType('rb'))
   parser.add_argument('--scale', type=int, default=8)
   parser.add_argument('--use_mic', action='store_true')
   parser.add_argument('--show_hi', action='store_true')
   parser.add_argument('--max_freq', type=int, default=20000)
   parser.add_argument('--min_freq', type=int, default=20)
   args = parser.parse_args()

   #Chunk determines the size of FFT, but also drives the refresh latency because each FFT output is displayed to the LEDs
   # If chunk is too small, the lower columns may map to the same bins (at 8192, column 0 is only 2 bins)
   chunk = 8192
   #Number of LED columns available.  The frequencies/bins assigned to each column will grow or shrink based on this variable
   num_columns = 16

   #Setup the LED display for writing outputs
   display = Matrix16x8.Matrix16x8()
   display.begin()
   display.clear()
   display.set_brightness(1)
   display.write_display()

   #Used during Raspberry PI headless operation to verify operation of LEDs and successful boot
   if (args.show_hi == True):
      display.write_hi()
      display.write_display()
      time.sleep(15)
      display.clear()
      display.write_display()   

   if (args.use_mic == True):
      #Setup an AlsaAudio stream to read data from microphone
      # Already configured using alsamixer and alsarecord
      input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK, cardindex=1)
      input.setchannels(1)
      sample_rate = 44100
      input.setrate(sample_rate)
      input.setformat(aa.PCM_FORMAT_S16_LE)
      input.setperiodsize(chunk//8)
      #Needed to use a lambda for wave readframes() (see below)
      # So also use one here so the calls will have the same syntax
      read_data_func = lambda x,y: mic.read_mic(y, x)
   else:
      #Setup for reading from a .wav file on disk
      input = wave.open(args.wavfile)
      #The alsaaudio input object returns two values in NON_BLOCKING_MODE
      # Use a lambda function to coerce the wave readframes() function to return the same type
      read_data_func = lambda x,y: (1, x.readframes(y))
      sample_rate = input.getframerate()
      print("Input File Sample Rate ", sample_rate)
      #Also setup to play the .wav file through the Raspberry pi audio output
      output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NONBLOCK)
      output.setchannels(1)
      output.setperiodsize(chunk)

   #Precompute which bins/frequencies will map to each LED column to save processing time during the loop
   bin_mapping = spectrum.find_bin_mapping_np(num_columns, args.min_freq, args.max_freq, chunk, sample_rate)

   # Loop through the wave file or mic input
   loop = 1
   while loop == 1:
      #Call the function pointer that will either read from mic or file on disk
      data = read_data_func(input, chunk)
      # At the end of a .wav file, data will be '', so break out of the processing loop
      if (len(data) == 0): break

      # Optional scale factor is applied to output of FFT
      #  8 is default for full scale 16-bit audio, increase if volume is low
      bin_powers = spectrum.get_spectrum(data, bin_mapping, chunk, args.scale)
      #Depending on scale factor and input power level result may overdrive the LED height
      #Clip here to prevent overflow in LED code.
      np.clip(bin_powers,0,8,bin_powers)
      
      #Use the set_column function to more efficiently write out all LED data compared to setting each pixel individually
      for col in range(0,num_columns):
         display.set_column(col, bin_powers[col])
      display.write_display()
