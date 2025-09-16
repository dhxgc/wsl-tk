import configparser
import os
import subprocess

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

checkConfig()

config = configparser.ConfigParser()
config.read(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini")

defaultPath = config.get('General', 'defaultPath')
interfaceScale = config.getfloat('General', 'interfaceScale')