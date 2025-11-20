import subprocess
import os
from fastapi import APIRouter

router = APIRouter(prefix="/player", tags=["player"])

MUSIC_DIR = os.environ.get("MUSIC_DIR", "/music")

@router.get("/play")
def play(path: str):
    # IMPORTANT: The path from the database should be relative to the music directory.
    # For example, if your music is in /home/user/music/song.mp3, and you mount
    # /home/user/music to /music in the container, the path in the database
    # should be "song.mp3".
    full_path = os.path.join(MUSIC_DIR, path)
    subprocess.run(["mpv", full_path, "--fullscreen"])
    return {"status": "playing", "file": full_path}

