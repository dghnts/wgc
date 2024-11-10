import subprocess
import sys


def convert_path(path):
    if sys.platform == "linux":
        return subprocess.check_output(["wslpath", path]).strip()
    return path
