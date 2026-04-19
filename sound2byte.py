#!/usr/bin/env python3
"""
sound2bytebeat - Convert any WAV file to a bytebeat formula that plays the exact sound
Usage: python sound2bytebeat.py input.wav
"""

import wave
import struct
import sys
import os

def wav_to_bytebeat(wav_file):
    # Check if file exists
    if not os.path.exists(wav_file):
        print(f"Error: File '{wav_file}' not found")
        sys.exit(1)
    
    # Open WAV file
    wav = wave.open(wav_file, 'rb')
    
    # Get WAV info
    channels = wav.getnchannels()
    sample_width = wav.getsampwidth()
    frame_rate = wav.getframerate()
    frames = wav.getnframes()
    
    print(f"Channels: {channels}, Sample width: {sample_width}, Frame rate: {frame_rate}, Frames: {frames}", file=sys.stderr)
    
    # Read all frames
    raw_data = wav.readframes(frames)
    
    # Convert to 8-bit samples (0-255)
    if sample_width == 1:
        # Already 8-bit
        samples = list(struct.unpack(f'{frames * channels}B', raw_data))
    elif sample_width == 2:
        # 16-bit to 8-bit
        samples_16 = struct.unpack(f'{frames * channels}h', raw_data)
        samples = [((s + 32768) >> 8) for s in samples_16]
    else:
        print(f"Unsupported sample width: {sample_width}")
        sys.exit(1)
    
    # Convert to mono if stereo (average left and right)
    if channels == 2:
        mono_samples = []
        for i in range(0, len(samples), 2):
            mono_samples.append((samples[i] + samples[i+1]) // 2)
        samples = mono_samples
        frames = len(samples)
    
    print(f"Converted to mono 8-bit, {frames} samples", file=sys.stderr)
    
    # Limit to reasonable length (max 65536 samples = ~8 seconds at 8kHz)
    MAX_SAMPLES = 65536
    if frames > MAX_SAMPLES:
        print(f"Warning: Sound is {frames} samples, truncating to {MAX_SAMPLES}", file=sys.stderr)
        samples = samples[:MAX_SAMPLES]
        frames = MAX_SAMPLES
    
    # Build the bytebeat formula using modulo indexing
    # Format: (sample0,sample1,sample2,...)[t % frames]
    samples_str = ','.join(str(s) for s in samples)
    formula = f"({samples_str})[t % {frames}]"
    
    # Output the formula
    print(formula)
    
    # Also output as C-style for compatibility
    print(f"\n// Alternative C-style formula:", file=sys.stderr)
    c_formula = f"((const unsigned char[%d]){{{samples_str}}})[t %% {frames}]" % frames
    print(c_formula, file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python sound2bytebeat.py input.wav")
        print("Converts WAV file to bytebeat formula")
        sys.exit(1)
    
    wav_to_bytebeat(sys.argv[1])
