from pathlib import Path
import pyge
from pyge import PyGE

if __name__ == "__main__":
    pyge = PyGE(Path(__file__).parent)
    pyge.start()
