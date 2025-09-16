from interface.root             import root
from interface.app_frame        import machineInfo
from system.wsl_functions       import listMachine

import tkinter as tk

def renewSidebar():
    sidebarDelete()
    sidebarCreate()

def sidebarDelete ():
    if hasattr(root, 'sidebarFrame'):
        root.sidebarFrame.destroy()

def sidebarCreate():
    root.sidebarFrame = tk.Frame(root, borderwidth=5, relief="ridge")
    varListMachine = listMachine()
    root.sidebarFrame.grid(
        row=0,
        column=0,
        sticky="nswe"
    )
    root.sidebarFrame.grid_columnconfigure(0, weight=1)
    
    for row, distroName in zip(range(len(varListMachine)), varListMachine):
        tk.Button(
            root.sidebarFrame,
            text=f"{distroName}",
            command=lambda name=distroName: machineInfo(name),
            font="Courier 12"
        ).grid(row=row, column=0, padx=5, pady=5, sticky="nwe")