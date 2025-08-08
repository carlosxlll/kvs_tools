# src/db.py
import json
import os
from pathlib import Path

# 使用XDG Base Directory Specification
# 优先使用 XDG_DATA_HOME，否则默认为 ~/.local/share/kvs/
def get_db_path() -> Path:
    xdg_data_home = os.getenv("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "kvs" / "commands.json"
    else:
        return Path.home() / ".local" / "share" / "kvs" / "commands.json"

def load_db() -> dict:
    db_path = get_db_path()
    if not db_path.exists():
        return {}
    try:
        with open(db_path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # 可以记录错误日志
        print(f"Error: Could not decode JSON from {db_path}. Database might be corrupt.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while loading DB: {e}")
        return {}

def save_db(db_data: dict):
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"An error occurred while saving DB: {e}")

