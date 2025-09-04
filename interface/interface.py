from interface.tk_functions import *
import system.settings

def guiMain():
    root = tk.Tk()
    root.title("GUI WSL")
    root.geometry(system.settings.interfaceResolution)
    root.tk.call('tk', 'scaling', system.settings.interfaceScale)
    root.eval('tk::PlaceWindow . center')

    topbarCreate(root=root)
    sidebarCreate(root=root)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=4)

    root.mainloop()