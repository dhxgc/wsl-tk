import subprocess
import configparser
import os

def initConfig():
    conf = configparser.ConfigParser()
    conf.read(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini")
    return conf

def getAppList (machineName: str):
    config = initConfig()
    try:
        result = config.options(f"{machineName}.App")
        return result
    except configparser.NoSectionError:
        return None

def delAppFromList (machineName: str, appName: str):
    config = initConfig()
    result = config.remove_option(f"{machineName}.App", appName)
    if not config.options(f"{machineName}.App"):
        config.remove_section(f"{machineName}.App")
    
    with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
        config.write(configfile)
    return 1

def getAppCommand(machineName: str, appName: str):
    config = initConfig()
    return config.get(f"{machineName}.App", appName)

def addAppToList(machineName: str, appName: str, command: str):
    config = initConfig()
    section = f"{machineName}.App"
    if not config.has_section(f"{machineName}.App"):
        config.add_section(section)

    result = config.set(section, appName, command)
    with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
        config.write(configfile)
    return 1

def removeAllApps (machineName: str):
    config = initConfig()
    section = f"{machineName}.App"
    if not config.has_section(section):
        return 1
    else:
        config.remove_section(section)
        with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
            config.write(configfile)
    return 1

def runApp(command: str):
    DETACHED_PROCESS = 0x00000008
    CREATE_NO_WINDOW = 0x08000000
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)

    return 1

def changeApp (machineName: str, appName: str, command: str):
    config = initConfig()
    section = f"{machineName}.App"
    config.set(section, appName, command)
    
    with open(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini", "w") as configfile:
        config.write(configfile)

    return 1