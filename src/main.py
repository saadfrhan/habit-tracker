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

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Write today's one-line habit entry (what you did / pledge): ").strip()
    if not text:
        print("No entry. Exiting.")
        sys.exit(1)
    entry = append_entry(text)
    print("Appended:", entry.strip())

if __name__ == "__main__":
    main()