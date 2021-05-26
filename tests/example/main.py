from pathlib import Path
from pyge import PyGE

if __name__ == "__main__":
    pyge = PyGE(Path(__file__).parent)
    pyge.start()
