from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import songs, player

app = FastAPI(title="Diynet KTV Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(songs.router)
app.include_router(player.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Diynet KTV Backend"}
