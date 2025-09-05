import subprocess
import configparser
import os

from settings import config

def getAppList (machineName: str):
    return config.options(f"{machineName}.App")

def delAppFromList (machineName: str, appName: str):
    result = config.remove_option(f"{machineName}.App", appName)
    if not config.options(f"{machineName}.App"):
        config.remove_section(f"{machineName}.App")
    
    with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
        config.write(configfile)
    return result

def getAppCommand(machineName: str, appName: str):
    return config.get(f"{machineName}.App", appName)

def addAppToList(machineName: str, appName: str, command: str):
    section = f"{machineName}.App"
    if not config.has_section(f"{machineName}.App"):
        config.add_section(section)

    result = config.set(section, appName, command)
    with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
        config.write(configfile)
    return result

print(addAppToList("machine1", "app1", "command_text"))