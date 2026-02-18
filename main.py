import os
import rich
from functools import lru_cache
from pathlib import Path
from typing import Generator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse

from app import get_music

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("app/frontend/index.html", "rb") as f:
        return f.read()

@app.get("/api/song")
def get_songlist():
    files = os.listdir("audio")
    response = [
        {
            "name" : filename.split("|")[0],
            "url" : f"/api/audio/{filename}/audio",
            "thumbnail" : f"/api/audio/{filename}/thumbnail",
            "duration" : filename.split("|")[1]
        } for filename in files
    ]
    return response

def get_media(song, media_type):
    files = os.listdir(f"audio/{song}")
    for filename in files:
        if media_type in filename:
            filepath = Path(f"audio/{song}/{filename}")
            file_extension = filename.split(".")[-1]
            media_type = f"audio/{file_extension}"
            # media_type = f"audio/mpeg"
            file_stat = filepath.stat()
            media = {
                "path" : filepath,
                "media_type" : media_type,
                "filename" : filename
            }
            rich.inspect(media)
            return media
    return None


@app.get("/api/audio/{song}/audio")
def get_audio(song):
    return FileResponse(**get_media(song, "audio"))

@app.get("/api/audio/{song}/thumbnail")
def get_thumbnail(song):
    return FileResponse(**get_media(song, "thumbnail"))

@app.get("/api/download_yt")
def dl_yt(link : str):
    get_music.download_audio(link)
    return True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

