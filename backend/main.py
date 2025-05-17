import threading
import time
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import os
import shutil
from backend.vocal_remover import process_song

# ✅ Define FastAPI app only once (no repeated imports)
app = FastAPI()

# Temporary upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🔧 Cleanup function that runs in background after response
def cleanup_files(file_paths: list, delay: int = 30):
    """Delete files after a delay (seconds)"""
    def delete():
        time.sleep(delay)
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)
        print("🧹 Cleanup complete.")
    threading.Thread(target=delete).start()

# ✅ Upload + stem selection + cleanup
@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    stem: str = Form("instrumental")
):
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_files = process_song(input_path)

    stem = stem.lower()
    if stem in output_files:
        response_path = output_files[stem]
        all_paths = list(output_files.values()) + [input_path]
        cleanup_files(all_paths, delay=60)  # delay in seconds

        return FileResponse(response_path, media_type="audio/mpeg", filename=os.path.basename(response_path))
    else:
        return {"error": "Invalid stem choice"}




