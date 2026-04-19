import sys
import os
from pydub import AudioSegment

def audio_to_bytebeat(audio_file):
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_channels(1).set_frame_rate(8000).set_sample_width(1)
    samples = list(audio.raw_data)[:65536]
    samples_str = ','.join(str(s) for s in samples)
    formula = f"({samples_str})[t % {len(samples)}]"
    
    print(formula)
    
    # Save to file
    with open('formula.txt', 'w') as f:
        f.write(formula)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python sound2bytebeat.py input.mp3")
        sys.exit(1)
    audio_to_bytebeat(sys.argv[1])
