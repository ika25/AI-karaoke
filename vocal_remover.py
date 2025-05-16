import os
import subprocess
from pydub import AudioSegment

# === CONFIGURATION ===

# Input MP3 file (must be in same folder or provide full path)
input_file = "Indila.mp3"  # Replace with your audio file
output_folder = "separated"

# === STEP 1: Run Demucs to separate stems ===
print("🎵 Running Demucs...")

demucs_command = [
    "python", "-m", "demucs",
    "--out", output_folder,
    input_file
]

subprocess.run(demucs_command, check=True)

# === STEP 2: Locate output folder ===
# E.g., separated/htdemucs/song_name/
song_name = os.path.splitext(os.path.basename(input_file))[0]
stem_path = os.path.join(output_folder, "htdemucs", song_name)

# === STEP 3: Combine drums + bass + other into instrumental.wav ===
print("🎛️  Combining stems into instrumental.wav...")

drums = AudioSegment.from_wav(os.path.join(stem_path, "drums.wav"))
bass = AudioSegment.from_wav(os.path.join(stem_path, "bass.wav"))
other = AudioSegment.from_wav(os.path.join(stem_path, "other.wav"))

# Mix the stems together (add them)
instrumental = drums.overlay(bass).overlay(other)

# Export as WAV
instrumental_wav_path = os.path.join(stem_path, "instrumental.wav")
instrumental.export(instrumental_wav_path, format="wav")

# === STEP 4: Convert WAV to MP3 ===
print("🎧 Converting to MP3...")

instrumental_mp3_path = instrumental_wav_path.replace(".wav", ".mp3")
instrumental.export(instrumental_mp3_path, format="mp3")

print("✅ Done! Instrumental MP3 saved at:")
print(instrumental_mp3_path)