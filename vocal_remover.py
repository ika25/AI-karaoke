import os
import subprocess

input_file = "Indila.mp3"  # Replace with your actual song
output_dir = "separated"

os.makedirs(output_dir, exist_ok=True)

# Run Demucs using 'python -m demucs' instead of raw 'demucs'
command = [
    "python", "-m", "demucs",
    "--two-stems", "vocals",
    "--out", output_dir,
    input_file
]

subprocess.run(command)

print(f"Done! Check the '{output_dir}' folder for separated audio.")