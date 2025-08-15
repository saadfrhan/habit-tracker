from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from habit import DB_PATH, add_entry, chart_daily, init_db, CHARTS_DIR
from datetime import datetime, UTC
import os
from typing import Optional

init_db()

app = Flask(__name__, template_folder="templates", static_folder="static")


def query_db(query: str, args: Optional[tuple[str]] = None, one: bool = False):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        if args is not None:
            cur.execute(query, args)
        else:
            cur.execute(query)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/chart.png")
def chart():
    chart_path = os.path.join(CHARTS_DIR, "stats_daily.png")
    if not os.path.exists(chart_path):
        chart_daily()
    return send_file(chart_path, mimetype="image/png")


@app.route("/add-entry", methods=["POST"])
def add_entry_ajax():
    text = request.form.get("text", "").strip()
    if text:
        add_entry(text)
        chart_daily()
        return jsonify(success=True, timestamp=datetime.now(UTC).isoformat(), text=text)
    return jsonify(success=False)


@app.route("/search")
def search_entries():
    q = request.args.get("q", "").strip()
    if q:
        rows = query_db(
            "SELECT timestamp, text FROM habits WHERE text LIKE ? ORDER BY timestamp DESC",
            (f"%{q}%",),
        )
    else:
        rows = query_db("SELECT timestamp, text FROM habits ORDER BY timestamp DESC")
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
