#!/usr/bin/env python3
"""
sound2bytebeat - Convert ANY audio file to a bytebeat formula
Requires: pip install pydub
"""

import sys
import os
from pydub import AudioSegment

def audio_to_bytebeat(audio_file):
    # Load any audio format
    audio = AudioSegment.from_file(audio_file)
    
    # Convert to mono, 8-bit, 8000 Hz
    audio = audio.set_channels(1).set_frame_rate(8000).set_sample_width(1)
    
    # Get raw samples (0-255)
    samples = list(audio.raw_data)
    
    # Limit to reasonable length (max 65536 samples)
    MAX_SAMPLES = 65536
    if len(samples) > MAX_SAMPLES:
        samples = samples[:MAX_SAMPLES]
    
    # Generate bytebeat formula
    samples_str = ','.join(str(s) for s in samples)
    formula = f"({samples_str})[t % {len(samples)}]"
    
    print(formula)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python sound2bytebeat.py input.mp3")
        sys.exit(1)
    
    audio_to_bytebeat(sys.argv[1])
