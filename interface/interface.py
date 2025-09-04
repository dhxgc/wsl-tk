from interface.tk_functions import *
import system.settings

# CLI Interface
def cliMain():
    menuChoice = -1
    while menuChoice != 0:
        menuChoice=int(input("1 - List\n2 - Copy\n3 - Delete\n0 - Exit\n> "))
        match menuChoice:
            case 1:
                listMachine()
            case 2:
                nameOfNewDistro = input("Name of virtual machine: ")
                pathFileForImport = input("Path of template: ")
                destinationPathForMachine = system.settings.defaultPath + nameOfNewDistro
                vhd=bool(int(input("> .tar = 0\n> .vhdx = 1\n> ")))
                copyMachine(nameOfNewDistro, destinationPathForMachine, originalPath=pathFileForImport, vhd=vhd)
            case 3:
                nameOfNewDistro = input("Name of virtual machine: ")
                unregisterMachine(nameOfNewDistro)
            case 0:
                print("exit")
                break
            case _:
                print("Unknown choice.")

def guiMain():
    root = tk.Tk()
    root.title("GUI WSL")
    root.geometry(system.settings.interfaceResolution)
    root.tk.call('tk', 'scaling', system.settings.interfaceScale)
    root.eval('tk::PlaceWindow . center')

    topbarCreate(root=root)
    sidebarCreate(root=root)

    root.mainloop()