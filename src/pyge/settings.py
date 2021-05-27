from pathlib import Path
import os


def get_path(key):
    PATHS = {}

    if os.environ.get("PYGE_PROJECT_PATH"):
        PATHS["project"] = Path(os.environ.get("PYGE_PROJECT_PATH"))
        PATHS["scenes"] = PATHS["project"] / "scenes"
        PATHS["assets"] = PATHS["project"] / "assets"
        PATHS["fonts"] = PATHS["assets"] / "fonts"

    return PATHS.get(key)
