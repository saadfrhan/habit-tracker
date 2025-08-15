#!/usr/bin/env python3
import sys
import sqlite3
import csv
from datetime import datetime, UTC
import matplotlib.pyplot as plt
import os

DB_DIR = os.environ.get("DB_DIR", "./data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "habits.db")

CHARTS_DIR = os.environ.get("CHARTS_DIR", "./charts")
os.makedirs(CHARTS_DIR, exist_ok=True)


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


def stats_daily():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for row in c.execute(
        """
        SELECT substr(timestamp, 1, 10) AS day, COUNT(*)
        FROM habits
        GROUP BY day
        ORDER BY day                
    """
    ):
        print(f"{row[0]} | {row[1]}")
    conn.close()


def stats_monthly():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for row in c.execute(
        """
        SELECT substr(timestamp, 1, 7) AS month, COUNT(*)
        FROM habits
        GROUP BY month
        ORDER BY month
    """
    ):
        print(f"{row[0]} | {row[1]}")
    conn.close()


def export_csv(filename: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT id, timestamp, text FROM habits ORDER BY id").fetchall()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "timestamp", "text"])
        writer.writerows(rows)
    conn.close()
    print(f"Exported {len(rows)} entries to {filename}.")


def chart_daily():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute(
        """
        SELECT substr(timestamp, 1, 10) AS day, COUNT(*)
        FROM habits
        GROUP BY day
        ORDER BY day
    """
    ).fetchall()
    conn.close()

    if not rows:
        print("No data to chart.")
        return

    dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in rows]
    counts = [row[1] for row in rows]
    date_labels = [d.strftime("%Y-%m-%d") for d in dates]
    plt.figure(figsize=(8, 4))  # pyright: ignore[reportUnknownMemberType]
    bars = plt.bar(  # pyright: ignore[reportUnknownMemberType]
        date_labels, counts, color="#3498db"
    )
    plt.xlabel("Date")  # pyright: ignore[reportUnknownMemberType]
    plt.ylabel("Entries")  # pyright: ignore[reportUnknownMemberType]
    plt.title("Daily Habit Entries")  # pyright: ignore[reportUnknownMemberType]
    plt.xticks(rotation=45, ha="right")  # pyright: ignore[reportUnknownMemberType]

    for bar, count in zip(bars, counts):  # pyright: ignore[reportUnknownVariableType]
        plt.text(  # pyright: ignore[reportUnknownMemberType]
            bar.get_x()  # type: ignore
            + bar.get_width() / 2,  # type: ignore
            bar.get_height(),  # type: ignore
            str(count),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    chart_path = os.path.join(CHARTS_DIR, "stats_daily.png")
    plt.tight_layout()
    plt.savefig(chart_path)  # pyright: ignore[reportUnknownMemberType]
    plt.close()
    print("Chart saved as stats_daily.png")


def main():
    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  add <text>               Add a new entry")
        print("  list                     List all entries")
        print("  search <keyword>         Search by keyword (case insensitive)")
        print("  search-date <YYYY-MM-DD> Search by exact date")
        print("  stats-daily              Show count per day")
        print("  stats-monthly            Show count per month")
        print("  export-csv               Export all entries to CSV")
        print("  chart-daily              Generates a PNG bar chart of daily counts")
        print(
            "  daily-update             Prompts for today's entry, updates DB, CSV and chart."
        )
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

    elif command == "stats-daily":
        stats_daily()

    elif command == "stats-monthly":
        stats_monthly()

    elif command == "export-csv":
        if len(sys.argv) < 3:
            print("Filename required.")
            sys.exit(1)
        export_csv(sys.argv[2])

    elif command == "chart-daily":
        chart_daily()

    elif command == "daily-update":
        entry = input("Today's entry: ").strip()
        if not entry:
            print("No entry. Exiting.")
            sys.exit(1)
        ts, txt = add_entry(entry)
        print(f"Added: {ts} | {txt}")

        print("\n=== Daily Stats ===")
        stats_daily()

        print("\n=== Monthly Stats ===")
        stats_monthly()

        export_csv("habits_export.csv")
        chart_daily()
        print("\nDaily update complete.")

    else:
        print("Unknown command:", command)
        sys.exit(1)


if __name__ == "__main__":
    main()
