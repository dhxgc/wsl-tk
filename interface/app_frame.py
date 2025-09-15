from interface.root             import root
from system.app_functions       import *
from system.wsl_functions       import getMachinePath, disableMachine, getRunningMachines

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def machineInfo (machineName: str):
    if hasattr(root, "frameMachineInfo"):
        root.frameMachineInfo.destroy()

# Правый фрейм
    root.frameMachineInfo = ttk.Frame(root, borderwidth=5, relief="ridge")
    root.frameMachineInfo.grid(
        row=0,
        column=1,
        sticky="nswe",
    )
    root.frameMachineInfo.grid_columnconfigure(0, weight=1)
    
# Заголовок, путь машины
    labelName = ttk.Label (
        root.frameMachineInfo,
        text=f"{machineName}",
        font='Courier 14 bold',
        anchor="center",
        relief="raised"
    )
    labelName.grid(row=0, column=0, sticky="we", padx=10, pady=5)
    
    mgmtFrame = ttk.Frame(root.frameMachineInfo)
    labelStatus = ttk.Label(
        mgmtFrame,
        text="Запущена" if machineName in getRunningMachines() else "Выключена",
        font='Courier 8',
    )
    buttonPathInfo1 = tk.Button (
        mgmtFrame,
        text="Machine location",
        font='Courier 10',
        command=lambda: runApp(f'explorer.exe {getMachinePath(machineName)}')
    )
    buttonDisableMachine = tk.Button(
        mgmtFrame,
        text="Shutdown",
        font='Courier 10',
        command=lambda: disableMachine(machineName)
    )
    mgmtFrame.grid(row=1, column=0, sticky="nwe")
    labelStatus.grid(row=0, column=0, sticky="nw", padx=10, pady=15)
    buttonPathInfo1.grid(row=1, column=0, sticky="nw", padx=10)
    buttonDisableMachine.grid(row=1, column=1, sticky="nw", padx=10)

# Подфрейм с приложениями
    createAppFrame(machineName)

def removeAppFrame():
    if hasattr(root, 'frameApp'):
        root.frameApp.destroy()
    return 1

def createAppFrame (machineName):
    root.frameApp = ttk.Frame(root.frameMachineInfo, borderwidth=5, relief="raised")
    root.frameApp.grid_columnconfigure(1, weight=1)
    root.frameApp.grid(
        row=2,
        column=0,
        sticky="we",
        padx=10,
        pady=10
    )
    appsLabel = ttk.Label (
        root.frameApp,
        text=f"Список приложений",
        font='Courier 10',
    )
    appsAdd = tk.Button(
        root.frameApp,
        text="Добавить",
        font="Courier 10",
        command=lambda: guiAddApp(machineName)
    )
    appsDel = tk.Button(
        root.frameApp,
        text="Удалить",
        font="Courier 10",
        command=lambda: guiDelApp(machineName)
    )
    appsLabel.grid(row=0, column=0)
    appsAdd.grid(row=0, column=2, padx=5, pady=15, sticky="we")
    appsDel.grid(row=0, column=3, padx=5, pady=15, sticky="we")

    apps_list = getAppList(machineName)
    if apps_list == None:
        appsDel.config(state="disabled")
    else:
        appsDel.config(state="normal")
        for apps, row in zip(apps_list, range(1, len(apps_list)+1)):
            label = ttk.Label(
                root.frameApp,
                text=apps,
                font="Courier 10",
                cursor="hand2",
            )
            label.grid(row=row, column=0, padx=15, pady=5, sticky="w")
            
            button1 = tk.Button(
                root.frameApp,
                text="Изменить",
                font="Courier 10",
                command=lambda app=apps: guiChangeApp(machineName, app)
            )
            button1.grid(row=row, column=2, padx=5, pady=5, sticky="we")
            button2 = tk.Button(
                root.frameApp,
                text="Запустить",
                font="Courier 10",
                command=lambda app=apps: runApp(getAppCommand(machineName, app))
            )
            button2.grid(row=row, column=3, padx=5, pady=5, sticky="we")

    return 1

def guiChangeApp (machineName: str, appName: str):
    subRoot = tk.Toplevel(root)
    subRoot.title(f"Изменить приложение {appName}")
    subRoot.grab_set()
    subRoot.focus_force()
    subRoot.grid_columnconfigure(0, weight=1)
    
    labelCommand = ttk.Label(
        subRoot,
        text="Введите команду для запуска приложения:"
    )
    strCommand = tk.StringVar(value=getAppCommand(machineName, appName))
    entryCommand = ttk.Entry(
        subRoot,
        textvariable=strCommand
    )
    labelCommand.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    entryCommand.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    print(getAppCommand(machineName, appName))

    def onOk ():
        if changeApp(machineName, appName, strCommand.get()):
            subRoot.destroy()
        else:
            messagebox.showerror("Ошибка", f"Во время добавления приложения произошла ошибка")
            subRoot.destroy()

    button_frame = ttk.Frame(subRoot)
    button_frame.grid(row=4, column=0, sticky="n", padx=5, pady=10)
    
    okButton = ttk.Button(button_frame, text="OK", command=onOk)
    okButton.pack(side=tk.LEFT, padx=5)
    cancelButton = ttk.Button(button_frame, text="Отмена", command=subRoot.destroy)
    cancelButton.pack(side=tk.LEFT, padx=5)

    return 1

def guiAddApp (machineName: str):
    subRoot = tk.Toplevel(root)
    subRoot.title("Добавить приложение")
    subRoot.grab_set()
    subRoot.focus_force()
    subRoot.grid_columnconfigure(0, weight=1)

    labelName = ttk.Label(
        subRoot,
        text="Введите имя приложения:"
    )
    strName = tk.StringVar()
    entryName = ttk.Entry(
        subRoot,
        textvariable=strName
    )
    labelCommand = ttk.Label(
        subRoot,
        text="Введите команду для запуска приложения:"
    )
    strCommand = tk.StringVar()
    entryCommand = ttk.Entry(
        subRoot,
        textvariable=strCommand
    )

    labelName.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    entryName.grid(row=1, column=0, padx=5, pady=5, sticky="we")
    labelCommand.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    entryCommand.grid(row=3, column=0, padx=5, pady=5, sticky="we")
    
    def onOk ():
        if addAppToList(machineName, strName.get(), strCommand.get()):
            removeAppFrame()
            createAppFrame(machineName)
            subRoot.destroy()
        else:
            messagebox.showerror("Ошибка", f"Во время добавления приложения произошла ошибка")
            subRoot.destroy()

    button_frame = ttk.Frame(subRoot)
    button_frame.grid(row=4, column=0, sticky="n", padx=5, pady=10)
    
    okButton = ttk.Button(button_frame, text="OK", command=onOk)
    okButton.pack(side=tk.LEFT, padx=5)
    cancelButton = ttk.Button(button_frame, text="Отмена", command=subRoot.destroy)
    cancelButton.pack(side=tk.LEFT, padx=5)

    return 1

def guiDelApp (machineName: str):
    subRoot = tk.Toplevel(root)
    subRoot.title("Удалить приложение")
    subRoot.grab_set()
    subRoot.focus_force()

    labelName = ttk.Label(
        subRoot,
        text="Выберите приложение для удаления:"
    )
    cmbChoiceApp = tk.StringVar(value=getAppList(machineName)[0])
    cmbListApp = ttk.Combobox(
        subRoot,
        values=getAppList(machineName),
        textvariable=cmbChoiceApp,
        state="readonly"
    )
    labelName.grid(row=0, column=0, padx=10, pady=5, sticky="new")
    cmbListApp.grid(row=1, column=0, padx=10, pady=10, sticky="new")

    def onOk ():
        if delAppFromList(machineName, cmbChoiceApp.get()):
            removeAppFrame()
            createAppFrame(machineName)
            subRoot.destroy()
        else:
            messagebox.showerror("Ошибка", f"Во время удаления приложения произошла ошибка")
            subRoot.destroy()

    button_frame = ttk.Frame(subRoot)
    button_frame.grid(row=2, column=0, sticky="n", padx=5, pady=10)
    
    okButton = ttk.Button(button_frame, text="OK", command=onOk)
    okButton.pack(side=tk.LEFT, padx=5)
    cancelButton = ttk.Button(button_frame, text="Отмена", command=subRoot.destroy)
    cancelButton.pack(side=tk.LEFT, padx=5)

    return 1

