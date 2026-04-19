import sys
from pydub import AudioSegment

audio = AudioSegment.from_file(sys.argv[1])
audio = audio.set_channels(1).set_frame_rate(44100).set_sample_width(1)
samples = list(audio.raw_data)[:65536]

samples_str = ','.join(str(s) for s in samples)
formula = f"({samples_str})[t % {len(samples)}]"

with open('formula.txt', 'w') as f:
    f.write(formula)

print(formula)
