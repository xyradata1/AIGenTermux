import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".aigentermux"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_config():
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
