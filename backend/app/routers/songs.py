from fastapi import APIRouter
from ..db import get_db

router = APIRouter(prefix="/songs", tags=["songs"])


@router.get("/search")
def search(keyword: str):
    db = get_db()
    rows = db.execute(
        "SELECT id, artist, title, path FROM songs WHERE title LIKE ? OR artist LIKE ? LIMIT 100",
        (f"%{keyword}%", f"%{keyword}%"),
    ).fetchall()

    return [dict(row) for row in rows]
