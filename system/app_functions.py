import subprocess
import configparser
import os

config = configparser.ConfigParser()
config.read(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini")

def getAppList (machineName: str):
    try:
        result = config.options(f"{machineName}.App")
        return result
    except configparser.NoSectionError:
        return None

def delAppFromList (machineName: str, appName: str):
    result = config.remove_option(f"{machineName}.App", appName)
    if not config.options(f"{machineName}.App"):
        config.remove_section(f"{machineName}.App")
    
    with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
        config.write(configfile)
    return 1

def getAppCommand(machineName: str, appName: str):
    return config.get(f"{machineName}.App", appName)

def addAppToList(machineName: str, appName: str, command: str):
    section = f"{machineName}.App"
    if not config.has_section(f"{machineName}.App"):
        config.add_section(section)

    result = config.set(section, appName, command)
    with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
        config.write(configfile)
    return 1

def removeAllApps (machineName: str):
    section = f"{machineName}.App"
    if not config.has_section(section):
        return 1
    else:
        config.remove_section(section)
        with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
            config.write(configfile)
    return 1

def runApp(command: str):
    run = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 1