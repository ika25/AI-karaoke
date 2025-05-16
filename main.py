from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import os
import shutil
from vocal_remover import process_song

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    stem: str = Form("instrumental")  # default option
):
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_files = process_song(input_path)

    # Return the selected stem
    stem = stem.lower()
    if stem in output_files:
        return FileResponse(output_files[stem], media_type="audio/mpeg", filename=f"{stem}.mp3" if stem == "instrumental" else f"{stem}.wav")
    else:
        return {"error": "Invalid stem choice"}

