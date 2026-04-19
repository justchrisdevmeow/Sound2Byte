#!/usr/bin/env python3
"""
sound2byte - Convert any audio file to a bytebeat formula
Usage: python sound2byte.py input.mp3 [--raw]
"""

import sys
import argparse
import struct
import wave
import os

def main():
    parser = argparse.ArgumentParser(description='Convert audio to bytebeat formula')
    parser.add_argument('input', help='Input audio file (WAV, MP3, FLAC, OGG)')
    parser.add_argument('--raw', action='store_true', help='Output raw samples as array (for very short sounds)')
    args = parser.parse_args()

    # Load audio
    samples = load_audio(args.input)
    
    if args.raw:
        # Output as raw sample array (simple lookup)
        print(f"sample[{len(samples)}] = {{{','.join(map(str, samples))}}}")
        print(f"for(int t=0;;t++) putchar(sample[t%{len(samples)}]);")
    else:
        # Output as bytebeat formula
        formula = generate_formula(samples)
        print(formula)

def load_audio(filename):
    """Load audio file and return 8-bit mono samples (0-255)"""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == '.wav':
        return load_wav(filename)
    else:
        return load_ffmpeg(filename)

def load_wav(filename):
    wav = wave.open(filename, 'rb')
    frames = wav.getnframes()
    rate = wav.getframerate()
    raw = wav.readframes(frames)
    
    if wav.getsampwidth() == 1:
        samples = list(struct.unpack(f'{frames}B', raw))
    elif wav.getsampwidth() == 2:
        samples = [max(0, min(255, (s >> 8) + 128)) for s in struct.unpack(f'{frames}h', raw)]
    else:
        raise ValueError("Unsupported sample width")
    
    # Convert to mono if stereo
    if wav.getnchannels() == 2:
        samples = [samples[i] for i in range(0, len(samples), 2)]
    
    return samples

def load_ffmpeg(filename):
    """Use ffmpeg to convert any audio to raw 8-bit PCM"""
    import subprocess
    import tempfile
    
    with tempfile.NamedTemporaryFile(suffix='.raw', delete=False) as f:
        tmpfile = f.name
    
    cmd = [
        'ffmpeg', '-i', filename, '-f', 'u8', '-acodec', 'pcm_u8',
        '-ar', '8000', '-ac', '1', '-y', tmpfile
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    
    with open(tmpfile, 'rb') as f:
        samples = list(f.read())
    
    os.unlink(tmpfile)
    return samples

def generate_formula(samples):
    """Generate bytebeat formula using bitwise trick"""
    # For short sounds, use direct lookup
    if len(samples) <= 256:
        return f'((t&0)|({samples[0]}))'  # placeholder - actual direct lookup
    
    # For longer sounds, use the (t-i)>>31 trick
    terms = []
    for i, s in enumerate(samples[:1000]):  # Limit to 1000 samples for sanity
        terms.append(f'((t-{i})>>31)*{s}')
    
    return '(' + '+'.join(terms) + ')'

if __name__ == '__main__':
    main()
