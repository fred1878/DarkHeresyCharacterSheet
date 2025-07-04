from __future__ import annotations

import configparser
from pathlib import Path
from typing import Optional

from models import Character

DEFAULT_ENCODING = "utf-8"


def load_character(path: str | Path) -> Character:
    """Load a character file from *path* and return a ``Character`` instance.

    If the file does not exist or is empty/malformed, an empty ``Character`` is returned.
    """
    cfg = configparser.ConfigParser()

    file_path = Path(path)
    if file_path.exists():
        with file_path.open("r", encoding=DEFAULT_ENCODING) as fp:
            cfg.read_file(fp)
    else:
        # Return a blank character if file does not exist
        return Character()

    return Character.from_config(cfg)


def save_character(character: Character, path: str | Path) -> None:
    """Serialize *character* to disk at *path* in ConfigParser INI format."""
    cfg = character.as_config()
    file_path = Path(path)
    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding=DEFAULT_ENCODING) as fp:
        cfg.write(fp)