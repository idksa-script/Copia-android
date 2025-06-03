import os
import pyudev
import subprocess
from pathlib import Path
import shutil
import notify2
from pyudev import device

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
    return respaldo
    
def crearMedia(rutaAndroid, rutaCopia):
    if not rutaAndroid.exists():
        print("Error carpeta no encontrada")
        exit()

    for raiz, _ , archivos in os.walk(rutaAndroid):
        for archivo in archivos:
            _, ext =os.path.splitext(archivo)

            if ext.lower() in extenciones:
                rutaOrigen = Path(raiz)/archivo
                rutaRelativa = Path(raiz).relative_to(rutaAndroid)
                rutaDestino = rutaCopia/rutaRelativa/archivo
                if not rutaDestino.parent.exists():
                    rutaDestino.parent.mkdir(parents=True, exist_ok=True)

                if not rutaDestino.exists():
                    shutil.copy2(rutaOrigen, rutaDestino)
    
    n = notify2.Notification("copiaAndroid",
                         "Ha concluido la copia de seguridad")
    n.show()

def scan_Android(ruta, extenciones):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb")
    monitor.start()
    while True:
        device = monitor.poll(timeout=1)
        if device and device.properties.get("ACTION") == "add" and android(device):
            nombre = get_Name_Android(device)
            launch_Rofi(nombre)
            rutaCopia = crearCarpeta(ruta, nombre)
            rutaAndroid = Path("/run/user/1000/gvfs/mtp:host=Xiaomi_Redmi_14C_5LGUTOLNT8USFIBU/Almacenamiento interno compartido")


ruta = "/home/idksa_script/Documentos" 
extenciones = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mkv", ".webm"}

if __name__ == "__main__":
    scan_Android(ruta, extenciones)
