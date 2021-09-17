from pathlib import Path
import os


def get_path(key):
    PATHS = {}

    if os.environ.get("PYGE_PROJECT_PATH"):
        PATHS["/"] = Path(os.environ.get("PYGE_PROJECT_PATH"))
        PATHS["/scenes"] = PATHS["/"] / "scenes"
        PATHS["/sprites"] = PATHS["/"] / "sprites"
        PATHS["/assets"] = PATHS["/"] / "assets"
        PATHS["/assets/fonts"] = PATHS["/assets"] / "fonts"
        PATHS["/assets/images"] = PATHS["/assets"] / "images"
        PATHS["/assets/audios"] = PATHS["/assets"] / "audios"
        PATHS["/assets/videos"] = PATHS["/assets"] / "videos"
        PATHS["/assets/sprites"] = PATHS["/assets"] / "sprites"

    return PATHS.get(key)
