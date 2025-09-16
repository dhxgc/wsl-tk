# Functions for WSL operations
import subprocess


def disableMachine (distrName: str):
    if distrName in getRunningMachines():
        result = subprocess.Popen(["wsl.exe", "-t", distrName], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        return result
    else:
        return 1

def getRunningMachines ():
    result = subprocess.run(["wsl", "--list", "--running"], capture_output=True, encoding="utf-16le", creationflags=subprocess.CREATE_NO_WINDOW)
    list = result.stdout.split("\n")
    list.pop(0); list.pop()
    return list

def getMachinePath (distrName):
    result = subprocess.run(
        ["powershell.exe", 
         "-Command", 
         "Get-ChildItem 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss' -Recurse |", 
         "ForEach-Object {Get-ItemProperty $_.PsPath | Select-Object DistributionName, BasePath}"],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    raw_result = result.stdout.splitlines()
    for lines in raw_result:
        if distrName+" " in lines:
            lines = lines.replace(distrName, "", 1)
            lines = lines.strip()
            if "\\\?\\" in lines:
                lines = lines.replace("\\\?\\", "")
            return lines

def listMachine():
    rawListMachine = subprocess.run(["wsl.exe", "--list"], capture_output=True, text=True, encoding="utf-16le", creationflags=subprocess.CREATE_NO_WINDOW)
    cleanListMachine = []
    for rawLine in rawListMachine.stdout.split('\n'):
        cleanLine = rawLine.split(' ')[0]
        cleanListMachine.append(cleanLine)
    
    # Удаление левых строк
    cleanListMachine.pop(-1)
    cleanListMachine.pop(0)

    return cleanListMachine

def addMachineFromFile(distrName: str, destinationPath: str, originalPath: str, vhdSign: str):
    if vhdSign == "tar":
        result = subprocess.run(["wsl.exe", "--import", distrName, destinationPath, originalPath], 
                                capture_output=True, 
                                text=True,
                                encoding='utf-16le',
                                creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        result = subprocess.run(["wsl.exe", "--import", distrName, destinationPath, originalPath, "--vhd"], 
                                capture_output=True, 
                                text=True,
                                encoding='utf-16le',
                                creationflags=subprocess.CREATE_NO_WINDOW)
    print(result.stdout)
    return 1
    
def unregisterMachine (distrName: str):
    subprocess.run(["wsl.exe", "--unregister", distrName], 
                        capture_output=True, 
                        text=True,
                        encoding='utf-16le',
                        creationflags=subprocess.CREATE_NO_WINDOW)
    return 1

def copyMachine (newDistroName: str, templateDistrName: str, pathOfNewDistro: str):
    subprocess.run(
        ["wsl.exe",
         "--import",
         f"{newDistroName}",
         f"{pathOfNewDistro}",
         f"{getMachinePath(templateDistrName)}\\ext4.vhdx",
         "--vhd"],
        capture_output=True, 
        text=True, 
        encoding="utf-16le",
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    return 1
