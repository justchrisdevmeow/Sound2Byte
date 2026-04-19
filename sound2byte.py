import sys
from pydub import AudioSegment

# Load and convert audio
audio = AudioSegment.from_file(sys.argv[1])
audio = audio.set_channels(1).set_frame_rate(8000).set_sample_width(1)
samples = list(audio.raw_data)[:65536]

# Pack all samples into one big integer
# Each sample is 8 bits, so shift by 8*i
packed = 0
for i, s in enumerate(samples):
    packed |= (s << (8 * i))

# Formula: shift right by (t % len) * 8, mask 0xFF
formula = f"(({packed} >> ((t % {len(samples)}) * 8)) & 255)"

with open('formula.txt', 'w') as f:
    f.write(formula)

# Also print for log
print(formula)
