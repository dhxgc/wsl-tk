from interface.tk_functions import *
import system.settings

def guiMain():
    root = tk.Tk()
    root.title("GUI WSL")
    # root.geometry(system.settings.interfaceResolution)
    root.tk.call('tk', 'scaling', system.settings.interfaceScale)
    root.eval('tk::PlaceWindow . center')

    topbarCreate(root=root)
    sidebarCreate(root=root)

    root.frameMachineInfo = ttk.Frame(root, borderwidth=5, relief="ridge")
    root.frameMachineInfo.grid_propagate(False)
    root.frameMachineInfo.grid(row=0, column=1, sticky="ns")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    root.mainloop()