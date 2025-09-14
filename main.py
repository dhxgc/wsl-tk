from system.settings    import interfaceScale
from interface.sidebar  import sidebarCreate
from interface.topbar   import topbarCreate
from interface.root     import root

from tkinter            import ttk
from tkinter            import messagebox
import tkinter          as tk

import os
if os.name == "nt":
    from ctypes import windll

def guiMain():
    root.title("GUI WSL")

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