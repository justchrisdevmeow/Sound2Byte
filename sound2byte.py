import numpy as np
import soundfile as sf
from scipy.signal import resample
import sys
import struct

def sound_to_bytebeat(input_file, output_file="99477_Every_End....mp3", target_rate=8000, method="direct"):
    """
    Convert any sound file to ByteBeat audio.
    
    Args:
        input_file: path to input sound (WAV, FLAC, OGG, etc.)
        output_file: output WAV file
        target_rate: ByteBeat sample rate (typical: 8000, 11025, 16000, 44100)
        method: 
            "direct" - use raw bytes from sound as bytebeat stream
            "xor" - t ^ (t>>something) using sound bytes
            "and" - t & (sound_bytes)
    """
    # Load audio
    data, samplerate = sf.read(input_file, always_2d=False)
    
    # Convert to mono if stereo
    if data.ndim > 1:
        data = np.mean(data, axis=1)
    
    # Resample to target_rate for bytebeat
    num_samples = int(len(data) * target_rate / samplerate)
    resampled = resample(data, num_samples)
    
    # Convert float (-1..1) to bytes (0..255)
    # We'll use 8-bit unsigned (PCM_U8)
    byte_data = np.clip((resampled + 1) * 127.5, 0, 255).astype(np.uint8)
    
    # Generate ByteBeat output
    t = np.arange(len(byte_data), dtype=np.uint32)
    
    if method == "direct":
        # Pure bytebeat from sound data
        output_bytes = byte_data
    elif method == "xor":
        # Classic bytebeat: t XOR (sound_byte)
        output_bytes = (t & 0xFF) ^ byte_data
    elif method == "and":
        output_bytes = (t & 0xFF) & byte_data
    elif method == "t_sound":
        # t AND sound byte
        output_bytes = t & byte_data
    else:
        # Custom: sound bytes as rhythm modulator
        output_bytes = (t >> 3) & byte_data
    
    # Convert back to float -1..1 for WAV
    output_float = (output_bytes.astype(np.float32) / 127.5) - 1.0
    
    # Write output
    sf.write(output_file, output_float, target_rate, subtype='PCM_16')
    print(f"ByteBeat written to {output_file} (rate={target_rate} Hz, method={method})")
    
    # Optional: also save raw bytes for other ByteBeat players
    with open(output_file.replace('.wav', '.raw'), 'wb') as f:
        f.write(output_bytes.tobytes())
    print(f"Raw bytes saved to {output_file.replace('.wav', '.raw')}")

# Example usage with different methods
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sound2bytebeat.py <input_sound_file> [method]")
        print("Methods: direct, xor, and, t_sound")
        sys.exit(1)
    
    input_sound = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "xor"
    
    sound_to_bytebeat(input_sound, target_rate=16000, method=method)
