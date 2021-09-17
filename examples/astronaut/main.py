from pathlib import Path

from yammy import Yammy

if __name__ == "__main__":
    yammy = Yammy(Path(__file__).parent)
    yammy.start()
