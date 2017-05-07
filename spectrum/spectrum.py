####################
# George Mason University - ECE612
# Aaron Joe Parrish - Spring 2017
#
# Final Project
#  spectrum.py
#  Implements a numpy FFT in Python 3.4
#  and scales the results to fit on an LED array
####################
import numpy as np

#samplerate:  Choose a sample rate of 44.1 KHz, the same sample rate used for audio CDs
#             From Nyquist, this samplerate will capture 20 KHz roughly the limit of human hearing
#chunk:       The size of each packet read from the microphone and the points of the subsequent FFT
#num_columns: The number of columns of LEDs that will display our spectrum
#
# Use this function to precompute the bin mapping and save the results outside
# of the main audio processing loop.
def find_bin_mapping_np(num_columns, min_freq, max_freq, chunk=4096, samplerate=44100):

    #Need to group and assign output bins of the FFT to each column
    #Since sound is logarithmic, we will assign equal amounts of log(spectrum)
    # to each column which will result in fewer bins for the lower columns

    #Audible frequency range is 20Hz - 20KHz
    #If we only had one column, it would cover the entire range
    bin_mapping = np.array([min_freq, max_freq])
    num_cols_mapped = 1

    #First, take the log of each entry
    bin_mapping = np.log10(bin_mapping)

    #As we add bins, insert values into bin_mapping
    while num_cols_mapped < num_columns:
        new_vals = np.array([])
        for i in range(num_cols_mapped):
            new_vals = np.append(new_vals, sum(bin_mapping[i:i+2]) / 2.0)
        #Interleave these values into bin_mapping
        bin_mapping = np.insert(bin_mapping, list(range(1,num_cols_mapped+1)), new_vals)
        #Double the number of columns mapped each iteration
        num_cols_mapped = num_cols_mapped * 2
    #Done mapping, but the bin_mapping list is still in log form
    #Use NumPy power() to convert back to frequency in Hz
    bin_freqs = np.power(10, bin_mapping)

    #Based on the number of points in our FFT, find the closest bin index to each frequency entry
    #Only the first half of the bins contain useful information and each bin has width of
    # (sampling_rate / chunk)
    bin_mapping = [int(round(x / (samplerate / chunk))) for x in bin_freqs]
    print("Selected Bin Mapping: ", bin_mapping)
    print("Selected Bin Freqs: ", bin_freqs)

    #So now, each column will average the FFT bins between each pair of indexes in bin_mapping
    return bin_mapping
    
# Data: Should be a chunk-length array of real samples to compute spectral data for
# bin_mapping: An array of bin indexes.  This function will scale and then sum the FFT output
#              between each bin_index and append to the output array
# chunk: Size of the FFT and the number of values in data
# scale: Optional argument with a default of 4.  Scales fft output by powers of 2
#        If set to 4 and the input is full scale 16-bit audio, should produce values between 0 and 8
#        Increase this parameter for audio data with low volume, or decrease to drive more than 8 LEDs per column
def get_spectrum(data, bin_mapping, chunk, scale=4):
   #Use the rfft function which only computes half of the FFT
   # Since our input is all real data, only the one half is useful
   y_fft = np.fft.rfft(data)
   # FFT returns complex float
   # Use abs() to get magnitude and then cast to int
   # Eventually mapping to just 8 LEDs, so okay to cast now and lose precision
   y_amp = (np.abs(y_fft)).astype(int)
   
   #After the FFT, the amplitudes are large.  On the order of 2^15 (Max input from Mic) * chunk
   # Dividing by (2^15 * chunk) would scale to between 0 and 1
   # But we want to drive LEDs of height 8, so don't divide by quite as much
   # Use right_shift to perform a faster divide-by-power-of-two
   y_shift = np.right_shift(y_amp, int(np.log2(chunk) + 15 - scale))

   bin_amplitudes = np.array([], dtype='i2')
   #Iterate through every item pair in bin_mapping using zip
   # Returns one item from each range on each iteration
   #  bin_mapping[:-1] iterates from beginning to last-1 item
   #  bin_mapping[1:]  iterates from second to last item
   for x,y in zip(bin_mapping[:-1],bin_mapping[1:]):
      #Sum energy between the indexes [x, y) and append to output array
      # Python [x:y] indexing does not include the y-th item
      amplitude = (np.sum(y_shift[x:y]))
      bin_amplitudes = np.append(bin_amplitudes, amplitude)

   # Loudness is logarithmic, so take the log2 of the bin powers
   bin_amplitudes = np.add(bin_amplitudes, np.ones(len(bin_amplitudes), int))
   bin_amplitudes = np.log2(bin_amplitudes).astype(int)

   return bin_amplitudes
