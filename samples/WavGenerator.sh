#!/bin/bash

python3 WavGenerator.py --freqs 2500 --amps 12384
python3 WavGenerator.py --freqs 1000 10000 --amps 8192 8192
python3 WavGenerator.py --freqs 20 200 2000 20000 --amps 1000 2000 3000 4000
