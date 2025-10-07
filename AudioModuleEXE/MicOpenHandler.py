import sys
import os

# Add parent directory to path so we can import Handler and Interface
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interface import start_interface
from Handler import VolumeController

if __name__ == "__main__":
    controller = VolumeController()
    start_interface(controller)
