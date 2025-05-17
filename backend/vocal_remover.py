import os
import subprocess
from pydub import AudioSegment

def process_song(input_file: str) -> dict:
    output_folder = "separated"
    print("🎵 Running Demucs...")

    # Step 1: Run Demucs separation
    demucs_command = [
        "python", "-m", "demucs",
        "--out", output_folder,
        input_file
    ]
    subprocess.run(demucs_command, check=True)

    # Step 2: Locate separated stems
    song_name = os.path.splitext(os.path.basename(input_file))[0]
    stem_path = os.path.join(output_folder, "htdemucs", song_name)

    # Load individual stems
    print("🎛️  Loading stems...")
    drums_path = os.path.join(stem_path, "drums.wav")
    bass_path = os.path.join(stem_path, "bass.wav")
    other_path = os.path.join(stem_path, "other.wav")
    vocals_path = os.path.join(stem_path, "vocals.wav")

    drums = AudioSegment.from_wav(drums_path)
    bass = AudioSegment.from_wav(bass_path)
    other = AudioSegment.from_wav(other_path)

    # Step 3: Combine stems for instrumental
    print("🎚️  Mixing instrumental...")
    instrumental = drums.overlay(bass).overlay(other)

    # Save as WAV
    instrumental_wav_path = os.path.join(stem_path, "instrumental.wav")
    instrumental.export(instrumental_wav_path, format="wav")

    # Step 4: Convert WAV to MP3
    instrumental_mp3_path = instrumental_wav_path.replace(".wav", ".mp3")
    instrumental.export(instrumental_mp3_path, format="mp3")

    print("✅ Processing complete!")

    # Return all relevant output paths
    return {
        "instrumental": instrumental_mp3_path,
        "vocals": vocals_path,
        "drums": drums_path,
        "bass": bass_path,
        "other": other_path
    }

