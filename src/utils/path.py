import os
from pprint import pprint

class Path:
    def __init__(self):
        self.UTILS = os.path.dirname(os.path.abspath(__file__))
        self.SRC = os.path.dirname(self.UTILS)
        self.ROOT = os.path.dirname(self.SRC)
        self.DATA = os.path.join(self.ROOT, 'data')
        self.SCRIPTS = os.path.join(self.SRC,'scripts')
        self.config = os.path.join(self.SRC, 'config.toml')
    
    def show(self):
        print(f"UTILS: {self.UTILS}")
        print(f"SRC: {self.SRC}")
        print(f"SCRIPTS: {self.SCRIPTS}")
        print(f"CONFIG: {self.config}")
        print(f"DATA: {self.DATA}")
        print(f"SCRIPTS: {self.SCRIPTS}")

if __name__ == '__main__':
    path = Path()
    path.show()
    
        