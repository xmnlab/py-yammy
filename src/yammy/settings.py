import os
from pathlib import Path


def get_path(key, subpath: str = ""):
    PATHS = {}

    if os.environ.get("YAMMY_PROJECT_PATH"):
        PATHS["/"] = Path(os.environ.get("YAMMY_PROJECT_PATH"))
        PATHS["/scenes"] = PATHS["/"] / "scenes"
        PATHS["/sprites"] = PATHS["/"] / "sprites"
        PATHS["/assets"] = PATHS["/"] / "assets"
        PATHS["/assets/fonts"] = PATHS["/assets"] / "fonts"
        PATHS["/assets/images"] = PATHS["/assets"] / "images"
        PATHS["/assets/audios"] = PATHS["/assets"] / "audios"
        PATHS["/assets/videos"] = PATHS["/assets"] / "videos"
        PATHS["/assets/sprites"] = PATHS["/assets"] / "sprites"

    if not subpath:
        return PATHS.get(key)

    return PATHS.get(key) / subpath.replace("/", os.sep)
