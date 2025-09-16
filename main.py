from system.settings        import interfaceScale
from system.wsl_functions   import listMachine

from interface.sidebar      import sidebarCreate, renewSidebar
from interface.app_frame    import machineInfo
from interface.topbar       import topbarCreate
from interface.root         import root

import tkinter as tk

import os
if os.name == "nt":
    from ctypes import windll

def guiMain():
    root.title("GUI WSL")
    root.bind("<KeyPress-F5>", lambda e: (renewSidebar(), machineInfo(root.selectedMachine)))

# Параметры запуска главного окна
    if os.name == "nt":
        windll.shcore.SetProcessDpiAwareness(1)
        root.tk.call('tk', 'scaling', interfaceScale * 1.3)
    elif os.name == "posix":
        root.tk.call('tk', 'scaling', interfaceScale * 1.3)
    
    root.eval('tk::PlaceWindow . center')

    topbarCreate()
    sidebarCreate()

    root.grid_columnconfigure(0, weight=1, minsize=300)
    root.grid_columnconfigure(1, weight=3, minsize=800)
    root.grid_rowconfigure(0, weight=1)

    root.mainloop()


if __name__=="__main__":
    guiMain()