from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("app/frontend/index.html", "rb") as f:
        return f.read()

@app.get("/api/song")
def get_song():
    files = os.listdir("audio")
    response = [
        {
            "name" : filename.split("|")[0],
            "url" : f"/api/audio/{filename}/audio",
            "thumbnail" : f"/api/audio/{filename}/thumbnail",
            "duration" : filename.split("|")[0]
        } for filename in files
    ]
    return response

@app.get("/api/audio/{song}/audio")
def get_audio(song):
    files = os.listdir(f"audio/{song}")
    for filename in files:
        if "audio" in filename:
            file_extension = filename.split(".")[-1]
            return FileResponse(f"audio/{song}/{filename}", media_type=f"audio/{file_extension}")
    return None

@app.get("/api/audio/{song}/thumbnail")
def get_thumbnail(song):
    files = os.listdir(f"audio/{song}")
    for filename in files:
        if "thumbnail" in filename:
            file_extension = filename.split(".")[-1]
            return FileResponse(f"audio/{song}/{filename}", media_type=f"audio/{file_extension}")
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

