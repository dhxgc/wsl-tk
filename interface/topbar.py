from interface.root             import root
from interface.sidebar          import sidebarCreate, sidebarDelete
from interface.app_frame        import removeAppFrame

from system.wsl_functions       import listMachine, addMachineFromFile, unregisterMachine, copyMachine
from system.app_functions       import removeAllApps, runApp
from system.settings            import defaultPath
from system.helper_functions    import selectFile


import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox


def topbarCreate():
    topbar = tk.Menu()
    root.config(menu=topbar)

# Actions
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

# Settings and other
    topbarSettings = tk.Menu(root, tearoff=False)
    topbarSettings.add_command(
        label="Открыть файл конфигурации",
        command=lambda: runApp(f'notepad.exe C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini')
    )
    topbar.add_cascade(menu=topbarSettings, label="Settings")

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
                removeAppFrame()
                removeAllApps(selectedMachine)
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