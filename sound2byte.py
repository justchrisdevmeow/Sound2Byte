import sys
import os
import numpy as np
from pydub import AudioSegment

def sound2bytebeat(input_file):
    # Load any audio format (mp3, wav, flac, ogg)
    audio = AudioSegment.from_file(input_file)
    
    # Convert to mono
    if audio.channels > 1:
        audio = audio.set_channels(1)
    
    # Get raw samples as numpy array (16-bit)
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    
    # Normalize to -1..1 range (for 16-bit audio)
    samples = samples / 32768.0
    
    # Convert to bytes (0-255)
    bytes_data = np.clip((samples + 1) * 127.5, 0, 255).astype(np.uint8)
    
    # Generate time
    t = np.arange(len(bytes_data))
    
    # Find best formula by brute force
    best_formula = None
    best_error = float('inf')
    
    # Try common ByteBeat patterns
    for shift in range(1, 12):
        for op in ['&', '^', '|']:
            try:
                if op == '&':
                    result = (t.astype(np.uint32) & (bytes_data >> shift)).astype(np.uint8)
                elif op == '^':
                    result = (t.astype(np.uint32) ^ (bytes_data >> shift)).astype(np.uint8)
                else:
                    result = (t.astype(np.uint32) | (bytes_data >> shift)).astype(np.uint8)
                
                error = np.abs(result.astype(int) - bytes_data.astype(int)).sum()
                
                if error < best_error:
                    best_error = error
                    best_formula = f"t {op} (sound >> {shift})"
            except:
                pass
    
    # Also try t >> shift variations
    for shift in range(1, 12):
        try:
            result = ((t >> shift).astype(np.uint32) & bytes_data).astype(np.uint8)
            error = np.abs(result.astype(int) - bytes_data.astype(int)).sum()
            if error < best_error:
                best_error = error
                best_formula = f"(t >> {shift}) & sound"
        except:
            pass
    
    return best_formula, best_error

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sound2byte.py <audio_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        # Try common names if not found
        for name in ["sound.mp3", "sound.wav", "sound.flac", "sound.ogg"]:
            if os.path.exists(name):
                input_file = name
                break
        else:
            print(f"File not found: {input_file}")
            sys.exit(1)
    
    print(f"Processing: {input_file}")
    formula, error = sound2bytebeat(input_file)
    
    # Write formula to formula.txt
    with open("formula.txt", "w") as f:
        f.write(f"// ByteBeat formula from {input_file}\n")
        f.write(f"// Error: {error}\n")
        f.write(f"{formula}\n")
    
    print(f"Formula written to formula.txt: {formula}")
