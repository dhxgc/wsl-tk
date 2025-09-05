from tkinter import filedialog as fd
import subprocess
import re
import os


def checkConfig():
    defaultConfig = f'''[General]
defaultPath     = C:/Users/{os.getlogin()}/WSL/
interfaceScale  = 2

'''
    if os.name == "nt":
        if os.path.exists(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini"):
            return 1
        else:
            subprocess.run(["powershell.exe", "-Command", "mkdir", "-p", f"C:/Users/{os.getlogin()}/.config/wsl-tk"], text=True, capture_output=True)
            with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", 'w') as config:
                config.write(defaultConfig)
                return 0

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
        initialdir='/',
        filetypes=filetypes
    )
    if re.search(r"\/mnt\/.\/", filename):
        return nixToWinPath(filename)
    else:
        return filename
    
def copyToClipboard (e, root, text):
    root.clipboard_clear()
    root.clipboard_append(text)