#!/usr/bin/env python3
import sys
import sqlite3
from datetime import datetime, UTC
from pathlib import Path

DB_PATH = Path("habits.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            text TEXT NOT NULL      
        )
    """
    )
    conn.commit()
    conn.close()


def add_entry(text: str):
    ts = datetime.now(UTC).isoformat(timespec="seconds") + "Z"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO habits (timestamp, text) VALUES (?, ?)", (ts, text.strip()))
    conn.commit()
    conn.close()
    return ts, text.strip()


def list_entries():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for row in c.execute("SELECT id, timestamp, text FROM habits ORDER BY id"):
        print(f"{row[0]} | {row[1]} | {row[2]}")
    conn.close()


def search_entries(keyword: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for row in c.execute(
        "SELECT id, timestamp, text FROM habits WHERE text LIKE ?", (f"%{keyword}%",)
    ):
        print(f"{row[0]} | {row[1]} | {row[2]}")
    conn.close()


def search_by_date(date_str: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for row in c.execute(
        "SELECT id, timestamp, text FROM habits WHERE timestamp LIKE ?",
        (f"{date_str}%",),
    ):
        print(f"{row[0]} | {row[1]} | {row[2]}")
    conn.close()


def main():
    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  add <text>               Add a new entry")
        print("  list                     List all entries")
        print("  search <keyword>         Search by keyword (case insensitive)")
        print("  search-date <YYYY-MM-DD> Search by exact date")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
        else:
            text = input("Habit entry: ").strip()
        if not text:
            print("No entry. Exiting.")
            sys.exit(1)
        ts, txt = add_entry(text)
        print(f"Added: {ts} | {txt}")

    elif command == "list":
        list_entries()

    elif command == "search":
        if len(sys.argv) < 3:
            print("Keyword required.")
            sys.exit(1)
        search_entries(sys.argv[2])

    elif command == "search-date":
        if len(sys.argv) < 3:
            print("Date required (YYYY-MM-DD).")
            sys.exit(1)
        search_by_date(sys.argv[2])

    else:
        print("Unknown command:", command)
        sys.exit(1)


if __name__ == "__main__":
    main()
