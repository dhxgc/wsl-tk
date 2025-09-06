from system.wsl_functions import *
from system.helper_functions import *

from system.settings import defaultPath

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Interfaces functions
def topbarCreate(root):
    topbar = tk.Menu()
    root.config(menu=topbar)

    topbarActions = tk.Menu(topbar, tearoff=False)
    topbarActions.add_command(
        label="Добавить",
        command=lambda: guiAddMachine(rootWindow=root)
    )
    topbarActions.add_command(
        label="Склонировать",
        command=lambda: guiCopyMachine(root=root)
    )
    topbarActions.add_command(
        label="Удалить",
        command=lambda: guiUnregisterMachine(root=root)
    )
    topbar.add_cascade(menu=topbarActions, label="Actions")

def sidebarDelete (root):
    if hasattr(root, 'sidebarFrame'):
        root.sidebarFrame.destroy()

def sidebarCreate(root):
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
            command=lambda name=distroName: machineInfo(root, name)
        ).pack(fill="x")

def machineInfo (root, machineName: str):
    if hasattr(root, "frameMachineInfo"):
        root.frameMachineInfo.destroy()
    
    root.frameMachineInfo = ttk.Frame(root, borderwidth=5, relief="ridge")
    root.frameMachineInfo.grid(
        row=0,
        column=1,
        sticky="ns",
    )
    
    labelName = ttk.Label (
        root.frameMachineInfo,
        text=f"{machineName}",
        font='Helvetica 14 bold',
        width=40,
        anchor="center",
        relief="raised"
    )
    text = "Machine location (Click to copy)"
    labelPathInfo1 = ttk.Label (
        root.frameMachineInfo,
        text=text,
        font='Helvetica 8 bold',
        cursor="hand2"
    )
    labelName.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    labelPathInfo1.grid(row=1, column=0, sticky="nw", padx=10)
    labelPathInfo1.bind("<Button-1>", lambda e: copyToClipboard(e, root, getMachinePath(machineName)))

# Кнопки для топбара
def guiAddMachine(rootWindow):
    subRoot = tk.Toplevel(rootWindow)
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
            sidebarDelete(root=rootWindow)
            sidebarCreate(root=rootWindow)
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
    
def guiCopyMachine(root):
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
            sidebarDelete(root=root)
            sidebarCreate(root=root)
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

def guiUnregisterMachine(root):
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
                sidebarDelete(root=root)
                sidebarCreate(root=root)
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