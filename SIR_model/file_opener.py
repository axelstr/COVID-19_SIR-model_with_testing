import sys
import os
import subprocess


def openFile(fileName):
    if sys.platform == "win32":
        os.startfile(fileName, 'open')
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, fileName])
