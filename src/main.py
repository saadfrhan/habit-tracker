#!/usr/bin/env python3
import sys
from datetime import datetime, UTC
from pathlib import Path

LOG = Path("habits.log")

def append_entry(text: str):
    ts = datetime.now(UTC).isoformat(timespec='seconds') + "Z"
    entry = f"{ts} - {text.strip()}\n"
    LOG.write_text(
        LOG.read_text() + entry if LOG.exists() else entry, encoding="utf-8"
    )
    return entry

def list_entries():
    if not LOG.exists():
        print("No entries found.")
        return
    print(LOG.read_text(), end="")

def search_entries(keyword: str):
    if not LOG.exists():
        print("No entries found.")
        return
    keyword_lower = keyword.lower()
    for line in LOG.read_text().splitlines():
        if keyword_lower in line.lower():
            print(line)

def search_by_date(date_str: str):
    if not LOG.exists():
        print("No entries found.")
        return
    for line in LOG.read_text().splitlines():
        if line.startswith(date_str):
            print(line)

def main():
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
        entry = append_entry(text)
        print("Appended:", entry.strip())

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