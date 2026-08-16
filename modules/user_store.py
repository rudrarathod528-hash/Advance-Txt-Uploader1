"""
user_store.py — Persistent JSON-based storage for users and groups.
Bot restart par data reset nahi hoga.
"""
import json
import os

_STORE_FILE = "user_store.json"

def _load() -> dict:
    if os.path.exists(_STORE_FILE):
        try:
            with open(_STORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"users": [], "groups": []}

def _save(data: dict):
    try:
        with open(_STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[user_store] Save error: {e}")

def register_user(user_id: int):
    data = _load()
    if user_id not in data["users"]:
        data["users"].append(user_id)
        _save(data)

def register_group(chat_id: int):
    data = _load()
    if chat_id not in data["groups"]:
        data["groups"].append(chat_id)
        _save(data)

def get_all_users() -> list:
    return list(_load()["users"])

def get_all_groups() -> list:
    return list(_load()["groups"])

def get_all_targets() -> list:
    """Return users + groups combined (for broadcast)."""
    data = _load()
    return list(set(data["users"] + data["groups"]))
