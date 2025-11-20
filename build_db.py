import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "songs.db"
CSV_PATH = BASE_DIR / "database" / "ktv_songs.csv"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            title TEXT,
            path TEXT
        )
        """
    )
    conn.commit()
    return conn


def load_csv(conn):
    with CSV_PATH.open(newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [
            (row.get("artist", ""), row.get("title", ""), row.get("path", ""))
            for row in reader
        ]
    conn.executemany(
        "INSERT INTO songs (artist, title, path) VALUES (?, ?, ?)",
        rows,
    )
    conn.commit()


def main():
    conn = init_db()
    load_csv(conn)
    print("songs.db generated successfully")


if __name__ == "__main__":
    main()
