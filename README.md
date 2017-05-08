# raspi-spectrogram
Live Audio Visualizer (Microphone -> LED Array) implemented in Python 3.4 for Raspbian Jessie

To execute:
python3 main.py

The following command line arguments are available:

"--wavfile" Use with a path to a readable .wav file.  Instead of processing microphone data, the program will read that file.

"--scale" Sets the scaling factor applied to the FFT output.  Default value of 8

"--use_mic" Set this flag to process microphone data.  Must use either --use_mic or --wavfile

"--show_hi" For headless RPi operation, will display a "HI" message on the LEDs for 15 seconds on program start

"--max_freq" Use with an integer from 0 to 22000.  Sets the upper frequency range that will be processed and assigned to the leftmost column.  Default 20000.

"--min_freq" Use with an integer from 0 to 22000.  Must be less than --max_freq.  Sets lower frequency processing range.  Default 20
