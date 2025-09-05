from interface.tk_functions import *
import system.settings

if os.name == "nt":
    from ctypes import windll

def guiMain():
    root = tk.Tk()
    root.title("GUI WSL")
    
    if os.name == "nt":
        windll.shcore.SetProcessDpiAwareness(1)
        root.tk.call('tk', 'scaling', system.settings.interfaceScale * 1.3)
    elif os.name == "posix":
        root.tk.call('tk', 'scaling', system.settings.interfaceScale * 1.3)
    
    # root.geometry(system.settings.interfaceResolution)
    root.eval('tk::PlaceWindow . center')

    topbarCreate(root=root)
    sidebarCreate(root=root)

    root.frameMachineInfo = ttk.Frame(root, borderwidth=5, relief="ridge")
    root.frameMachineInfo.grid_propagate(False)
    root.frameMachineInfo.grid(row=0, column=1, sticky="ns")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    root.mainloop()