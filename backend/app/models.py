from pydantic import BaseModel


class Song(BaseModel):
    id: int
    artist: str
    title: str
    path: str
