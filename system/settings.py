import configparser
import os

from helper_functions import *

# Проверка конфиги, создание
checkConfig()

config = configparser.ConfigParser()
config.read(f"C:/Users/{os.getlogin()}/.config/wsl-tk/config.ini")

defaultPath = config.get('General', 'defaultPath')
# defaultPath = f"C:/Users/{os.getlogin()}/WSL/"
interfaceScale = config.getfloat('General', 'interfaceScale')