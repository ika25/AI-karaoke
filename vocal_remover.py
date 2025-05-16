# vocal_remover.py

import os
import subprocess
from pydub import AudioSegment

def process_song(input_file: str) -> str:
    output_folder = "separated"
    print("🎵 Running Demucs...")

    # Step 1: Run Demucs
    demucs_command = [
        "python", "-m", "demucs",
        "--out", output_folder,
        input_file
    ]
    subprocess.run(demucs_command, check=True)

    # Step 2: Locate stems
    song_name = os.path.splitext(os.path.basename(input_file))[0]
    stem_path = os.path.join(output_folder, "htdemucs", song_name)

    print("🎛️  Combining stems into instrumental.wav...")
    drums = AudioSegment.from_wav(os.path.join(stem_path, "drums.wav"))
    bass = AudioSegment.from_wav(os.path.join(stem_path, "bass.wav"))
    other = AudioSegment.from_wav(os.path.join(stem_path, "other.wav"))

    instrumental = drums.overlay(bass).overlay(other)

    instrumental_wav_path = os.path.join(stem_path, "instrumental.wav")
    instrumental.export(instrumental_wav_path, format="wav")

    # Step 3: Convert to MP3
    print("🎧 Converting to MP3...")
    instrumental_mp3_path = instrumental_wav_path.replace(".wav", ".mp3")
    instrumental.export(instrumental_mp3_path, format="mp3")

    print("✅ Done! Returning instrumental MP3 path.")
    return instrumental_mp3_path
