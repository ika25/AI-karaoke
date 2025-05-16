from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import shutil
from vocal_remover import process_song

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Vocal Remover API 🎶"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save uploaded file to temp directory
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call processing function to generate instrumental
    output_mp3 = process_song(input_path)

    # Return the final MP3 file
    return FileResponse(output_mp3, media_type="audio/mpeg", filename="instrumental.mp3")
