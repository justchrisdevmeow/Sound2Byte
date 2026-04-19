import sys
from pydub import AudioSegment

# Load and convert audio
audio = AudioSegment.from_file(sys.argv[1])
audio = audio.set_channels(1).set_frame_rate(8000).set_sample_width(1)
samples = list(audio.raw_data)

# Limit to 500 samples to avoid huge integers
MAX_SAMPLES = 500
if len(samples) > MAX_SAMPLES:
    samples = samples[:MAX_SAMPLES]

# Build the formula directly using string concatenation
# instead of building giant integer first
formula_parts = []
for i, s in enumerate(samples):
    formula_parts.append(f"((t%{len(samples)}=={i})*{s})")

formula = "+".join(formula_parts)

with open('formula.txt', 'w') as f:
    f.write(formula)

print(formula)
