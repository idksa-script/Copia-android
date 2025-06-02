from os.path import exists
from re import sub
import pyudev
import subprocess
import os

def get_Name_Android(device):
    name = device.get("ID_MODEL")
    return name

def android(device):
    model = device.get("ID_MODEL_ID")
    return model == "ff40"

def launch_Rofi(nombre):
    resultado = subprocess.run(["./rofip.sh", nombre],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   text=True,
                   check=True 
                   )
    if resultado.stderr:
        exit()

def crearCarpeta(ruta, nombre):
    respaldo = Path(f"{ruta}/{nombre}")
    respaldo.mkdir(exist_ok=True)

def scan_Android():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb")
    monitor.start
    for action, device in monitor:
        if action == "add" and android(device):
            nombre = get_Name_Android(device)
            launch_Rofi(nombre)
            crearCarpeta(ruta, nombre)


ruta = "/home/idksa_script/Documentos" 

if __name__ == "__main__":
    scan_Android()
