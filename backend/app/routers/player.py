import os
from fastapi import APIRouter

router = APIRouter(prefix="/player", tags=["player"])


@router.get("/play")
def play(path: str):
    os.system(f'mpv "{path}" --fullscreen')
    return {"status": "playing", "file": path}
