from tkinter import filedialog as fd
import subprocess
import re
import os

from system.settings import defaultPath

def nixToWinPath(path: str) -> str:
    match = re.match(r"^/mnt/([a-zA-Z])/(.*)", path)
    if not match:
        return path
    drive, rest = match.groups()
    return f"{drive.upper()}:/{rest}"

def selectFile():
    filetypes = (
        ('Templates', '*.tar *.vhdx'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open files',
        initialdir=defaultPath,
        filetypes=filetypes
    )
    if re.search(r"\/mnt\/.\/", filename):
        return nixToWinPath(filename)
    else:
        return filename
    
def copyToClipboard (e, root, text):
    root.clipboard_clear()
    root.clipboard_append(text)