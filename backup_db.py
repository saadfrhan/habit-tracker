import os
import shutil
from datetime import datetime, UTC
from habit import DB_PATH

BACKUP_DIR = os.environ.get("BACKUP_DIR", "./backups")
os.makedirs(BACKUP_DIR, exist_ok=True)


def backup_db():
    if not os.path.exists(DB_PATH):
        print("No database found to back up.")
        return None

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"habits_{timestamp}.db")
    shutil.copy(DB_PATH, backup_file)
    print(f"✅ Backup created: {backup_file}")
    return backup_file


if __name__ == "__main__":
    backup_db()
