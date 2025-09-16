# wsl-tk
Simple GUI for basic operations with distro's

# TODO
 - Обработка ошибок в WSL-функциях, выводить лог в `messagebox.showerror`
 - Выбор DETACHED и CREATE_NO_WINDOW
 - Сделать процесс изменения/создания команды удобнее

 - Выключить машину
 - Отображение включенных машин


##  Сборка
```powershell
# Нужен pyinstaller: pip install pyinstaller
pyinstaller -w --onefile .\main.py
```

## Зависимости
```text
tkinter
```