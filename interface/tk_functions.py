from system.wsl_functions import *
from system.helper_functions import *
from system.app_functions import addAppToList, delAppFromList, getAppList

from system.settings import defaultPath, interfaceScale

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# main 
if os.name == "nt":
    from ctypes import windll

def guiMain():
    global root
    root = tk.Tk()
    root.title("GUI WSL")

# Параметры запуска главного окна
    if os.name == "nt":
        windll.shcore.SetProcessDpiAwareness(1)
        root.tk.call('tk', 'scaling', interfaceScale * 1.3)
    elif os.name == "posix":
        root.tk.call('tk', 'scaling', interfaceScale * 1.3)
    
    # root.geometry(system.settings.interfaceResolution)
    root.eval('tk::PlaceWindow . center')

    topbarCreate()
    sidebarCreate()

    root.grid_columnconfigure(0, weight=1, minsize=300)
    root.grid_columnconfigure(1, weight=3, minsize=800)

    root.mainloop()

# Логика создания/обновления топбара, левого фрейма
def topbarCreate():
    topbar = tk.Menu()
    root.config(menu=topbar)

    topbarActions = tk.Menu(topbar, tearoff=False)
    topbarActions.add_command(
        label="Добавить",
        command=lambda: guiAddMachine()
    )
    topbarActions.add_command(
        label="Склонировать",
        command=lambda: guiCopyMachine()
    )
    topbarActions.add_command(
        label="Удалить",
        command=lambda: guiUnregisterMachine()
    )
    topbar.add_cascade(menu=topbarActions, label="Actions")

def sidebarDelete ():
    if hasattr(root, 'sidebarFrame'):
        root.sidebarFrame.destroy()

def sidebarCreate():
    root.sidebarFrame = tk.Frame(root, borderwidth=5, relief="ridge")
    varListMachine = listMachine()
    root.sidebarFrame.grid(
        row=0,
        column=0,
        sticky="we"
    )
    
    for distroName in varListMachine:
        tk.Button(
            root.sidebarFrame,
            text=f"{distroName}",
            command=lambda name=distroName: machineInfo(name),
            font="Courier 12"
        ).pack(fill="x")

# Логика правого фрейма - информация, приложения
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
    text = "Machine location (Click to copy)"
    labelPathInfo1 = ttk.Label (
        root.frameMachineInfo,
        text=text,
        font='Courier 10',
        cursor="hand2",
    )
    labelName.grid(row=0, column=0, sticky="we", padx=10, pady=10)
    labelPathInfo1.grid(row=1, column=0, sticky="nw", padx=10)
    labelPathInfo1.bind("<Button-1>", lambda e: copyToClipboard(e, root, getMachinePath(machineName)))

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
    appsAdd.grid(row=0, column=2, padx=5, pady=5, sticky="we")
    appsDel.grid(row=0, column=3, padx=5, pady=5, sticky="we")

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
            label.bind("<Button-1>", lambda e: copyToClipboard(e, root, getMachinePath(machineName)))

            button = tk.Button(
                root.frameApp,
                text="Запустить",
                font="Courier 10",
                command=lambda: print("RUN")
            )
            button.grid(row=row, column=3, padx=5, pady=5, sticky="we")

    return 1

# Кнопки для топбара
def guiAddMachine():
    subRoot = tk.Toplevel(root)
    subRoot.title("Добавить машину")
    subRoot.grab_set()
    subRoot.focus_force()

# Имя новой машины
    labelNameOfNewDistro = ttk.Label(
        subRoot,
        text="Введите имя новой машины:"
    )
    strNameOfNewDistro = tk.StringVar()
    entryNameOfNewDistro = ttk.Entry(
        subRoot,
        textvariable=strNameOfNewDistro
    )
    labelNameOfNewDistro.pack(fill='x', padx=5, pady=5)
    entryNameOfNewDistro.pack(fill='x', padx=5, pady=5)

# Путь к новой машине
    labelPathOfNewDistro = ttk.Label(
        subRoot,
        text="Введите путь для хранения диска:"
    )
    strPathOfNewDistro = tk.StringVar(value=defaultPath)
    entryPathOfNewDistro = ttk.Entry(
        subRoot,
        textvariable=strPathOfNewDistro
    )
    labelPathOfNewDistro.pack(fill='x', padx=5, pady=5)
    entryPathOfNewDistro.pack(fill='x', padx=5, pady=5)

# Синхронизация имени и нового пути
    def update(*args):
        strPathOfNewDistro.set(value=defaultPath+strNameOfNewDistro.get())
    strNameOfNewDistro.trace_add("write", update)

# Кнопки для выбора типа оригинального темплейта
    labelTypeOfNewDistro = ttk.Label(
        subRoot,
        text="Выберите тип шаблона:"
    )
    vhdSign = tk.StringVar()
    vhdSignButtonTar = ttk.Radiobutton(
        subRoot,
        text="Шаблон в виде .tar архива",
        value="tar",
        variable=vhdSign
    )
    vhdSignButtonVHDX = ttk.Radiobutton(
        subRoot,
        text="Шаблон в виде .vhdx диска",
        value="vhdx",
        variable=vhdSign
    )
    labelTypeOfNewDistro.pack(fill='x', padx=5, pady=5)
    vhdSignButtonTar.pack(fill='x', padx=5, pady=5)
    vhdSignButtonVHDX.pack(fill='x', padx=5, pady=5)

# Путь к темплейту
    labelTemplateOfNewDistro = ttk.Label(
        subRoot,
        text="Введите путь до шаблона:"
    )
    frameTemplatePath = ttk.Frame(subRoot)
    strTemplateOfNewDistro = tk.StringVar()
    entryTemaplteOfNewDistro = ttk.Entry(
        frameTemplatePath,
        textvariable=strTemplateOfNewDistro,
        width=20
    )
    explorerButton = ttk.Button(
        frameTemplatePath,
        text="Найти",
        command=lambda: strTemplateOfNewDistro.set(selectFile())
    )
    labelTemplateOfNewDistro.pack(fill='x', padx=5, pady=5)
    frameTemplatePath.pack(fill='x', padx=5, pady=5)
    entryTemaplteOfNewDistro.pack(side=tk.LEFT, padx=5, pady=5)
    explorerButton.pack(side=tk.LEFT, padx=5, pady=5)

# Фрейм ОК и Отмена
    def onOk ():
        if addMachineFromFile(strNameOfNewDistro.get(), strPathOfNewDistro.get(), strTemplateOfNewDistro.get(), vhdSign.get()):
        # Обновление списка ВМ главного окна
            sidebarDelete()
            sidebarCreate()
            messagebox.showinfo("Успешно", f"Дистрибутив {strNameOfNewDistro.get()} добавлен.")
            subRoot.destroy()
        else:
            messagebox.showerror("Ошибка", f"Во время добавления дистрибутива {strNameOfNewDistro.get()} произошла ошибка")
            subRoot.destroy()

    button_frame = ttk.Frame(subRoot)
    button_frame.pack(padx=10, pady=10)
    
    okButton = ttk.Button(button_frame, text="OK", command=onOk)
    okButton.pack(side=tk.LEFT, padx=5)
    cancelButton = ttk.Button(button_frame, text="Отмена", command=subRoot.destroy)
    cancelButton.pack(side=tk.LEFT, padx=5)
    
def guiCopyMachine():
    subRoot = tk.Toplevel(root)
    subRoot.title("Скопировать машину")
    subRoot.grab_set()
    subRoot.focus_force()
    
# Имя дистрибутива
    labelNameDistro = ttk.Label(
        subRoot,
        text="Введите имя нового дистрибутива:"
    )
    subRoot.nameOfNewDistro = tk.StringVar()
    subRoot.entryNameOfNewDistro = ttk.Entry(
        subRoot,
        textvariable=subRoot.nameOfNewDistro
    )
    labelNameDistro.pack(fill='x', padx=5, pady=5)
    subRoot.entryNameOfNewDistro.pack(fill='x', padx=5, pady=5)

# Выпадающий список всех машин
    labelChoiceMachine = ttk.Label(
        subRoot,
        text="Выберите машину для копирования:"
    )
    subRoot.cmbChoiceMachine = tk.StringVar(value=listMachine()[0])
    subRoot.cmbListMachine = ttk.Combobox(
        subRoot,
        values=listMachine(),
        textvariable=subRoot.cmbChoiceMachine,
        state="readonly"
    )
    labelChoiceMachine.pack(padx=10, pady=10, fill=tk.X)
    subRoot.cmbListMachine.pack(padx=10, pady=10, fill=tk.X)

# Путь к новой машине
    def updateEntry(*args):
    # После начала изменения поля имени получаем его содержимое и вставляем в переменную для поля пути
        temp = subRoot.nameOfNewDistro.get()
        subRoot.pathOfNewDistro.set(value=defaultPath+temp)
    # Отслеживание изменений в поле имени машины
    # При измененении вызывается updateEntry()
    subRoot.nameOfNewDistro.trace_add("write", updateEntry)

    labelDistroPath = ttk.Label(
        subRoot,
        text="Введите путь для хранения новой машины:"
    )
    subRoot.pathOfNewDistro = tk.StringVar(subRoot, value=defaultPath)
    subRoot.entryPathOfNewDistro = ttk.Entry(
        subRoot,
        textvariable=subRoot.pathOfNewDistro
    )
    labelDistroPath.pack(fill='x', padx=5, pady=5)
    subRoot.entryPathOfNewDistro.pack(fill='x', padx=5, pady=5)

# Фрейм с кнопками ОК и Отмена
    def onOk():
        if copyMachine(
            subRoot.nameOfNewDistro.get(),
            subRoot.cmbChoiceMachine.get(),
            subRoot.pathOfNewDistro.get()
        ):
        # Обновление списка ВМ главного окна
            sidebarDelete()
            sidebarCreate()
            messagebox.showinfo("Успешно", f"Дистрибутив {subRoot.nameOfNewDistro.get()} добавлен.")
            subRoot.destroy()
        else:
            messagebox.showerror("Ошибка", f"Во время копирования дистрибутива {subRoot.nameOfNewDistro.get()} произошла ошибка")
            subRoot.destroy()

    button_frame = ttk.Frame(subRoot)
    button_frame.pack(padx=10, pady=10)
    
    okButton = ttk.Button(button_frame, text="OK", command=onOk)
    okButton.pack(side=tk.LEFT, padx=5)
    cancelButton = ttk.Button(button_frame, text="Отмена", command=subRoot.destroy)
    cancelButton.pack(side=tk.LEFT, padx=5)

def guiUnregisterMachine():
    subRoot = tk.Toplevel(root)
    subRoot.title("Delete machine")
    subRoot.grab_set()
    subRoot.focus_force()

    mainInfoLabel = ttk.Label(subRoot, text="Выберите дистрибутив для удаления:")
    mainInfoLabel.pack(padx=10, pady=0, side=tk.TOP, fill=tk.X)

    machineValues = tuple(listMachine())
    listvariableMachines = tk.Variable(value=machineValues)
    listboxMachines = tk.Listbox(subRoot, listvariable=listvariableMachines, height=10)
    listboxMachines.pack(padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT)

    def onOk():
        # Получаем выбранный элемент
        selection = listboxMachines.curselection()
        if selection:
            selectedMachine = listboxMachines.get(selection[0])
            if unregisterMachine(selectedMachine):
            # Обновление списка ВМ главного окна
                sidebarDelete()
                sidebarCreate()
                messagebox.showinfo("Успешно", f"Дистрибутив {selectedMachine} удален.")
                subRoot.destroy()
            else:
                messagebox.showerror("Ошибка", f"Во время удаления дистрибутива {selectedMachine} произошла ошибка")
        else:
            messagebox.showwarning("Предупреждение", "Выберите дистрибутив для удаления")

    button_frame = ttk.Frame(subRoot)
    button_frame.pack(padx=10, pady=10)

    okButton = ttk.Button(button_frame, text="OK", command=onOk)
    okButton.pack(side=tk.RIGHT, padx=5)
    
    cancelButton = ttk.Button(button_frame, text="Отмена", command=subRoot.destroy)
    cancelButton.pack(side=tk.RIGHT, padx=5)

    return 0