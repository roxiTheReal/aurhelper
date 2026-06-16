import os
import subprocess
import tomllib

import tomli_w

CONFIG_DIR = os.path.join(os.path.expanduser("~/.config"), "calico")
CONFIG_PATH = os.path.join(CONFIG_DIR, "calico.toml")

DEFAULT_CONFIG = {"output": {"kibty": False}}


def load_config() -> dict:
    print(f"config path: {CONFIG_PATH}")
    print(f"exists: {os.path.exists(CONFIG_PATH)}")
    if not os.path.exists(CONFIG_PATH):
        print("creating config...")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_PATH, "rb") as f:
        return tomllib.load(f)


def save_config(config: dict) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "wb") as f:
        tomli_w.dump(config, f)


def open_config() -> None:
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)

    editor = os.environ.get("EDITOR", "nano")
    subprocess.run([editor, CONFIG_PATH])


def is_kibty_enabled() -> bool:
    config = load_config()
    return config.get("output", {}).get("kibty", False)
