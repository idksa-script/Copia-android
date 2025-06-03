import os
import pyudev
import subprocess
from pathlib import Path
import shutil
import notify2

RUTA_RESPALDO = "/home/idksa_script/Documentos"
EXTENCIONES = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mkv", ".webm"}
RUTA_ANDROID = Path("/run/user/1000/gvfs/mtp:host=Xiaomi_Redmi_14C_5LGUTOLNT8USFIBU/Almacenamiento interno compartido")

def get_Name_Android(device):
    return device.get("ID_MODEL", "Dispositivo desconocido").replace("_", " ")

def android(device):
    model = device.get("ID_MODEL_ID")
    return model == "ff40"

def launch_Rofi(nombre):
    try:
        subprocess.run(["./rofip.sh", nombre],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       text=True,
                       check=True)
    except subprocess.CalledProcessError:
        print("Error al ejecutar rofip.sh")
        exit()

def crearCarpeta(ruta, nombre):
    ruta_completa = Path(ruta) / nombre
    ruta_completa.mkdir(exist_ok=True)
    return ruta_completa

def crearMedia(rutaAndroid, rutaCopia):
    if not rutaAndroid.exists():
        print("Carpeta origen no encontrada")
        return

    print("Iniciando copia...\n")

    for raiz, _, archivos in os.walk(rutaAndroid):
        for archivo in archivos:
            _, ext = os.path.splitext(archivo)

            if ext.lower() in EXTENCIONES:
                rutaOrigen = Path(raiz) / archivo
                rutaRelativa = Path(raiz).relative_to(rutaAndroid)
                rutaDestino = rutaCopia / rutaRelativa / archivo

                if not rutaDestino.parent.exists():
                    rutaDestino.parent.mkdir(parents=True, exist_ok=True)

                if not rutaDestino.exists():
                    shutil.copy2(rutaOrigen, rutaDestino)

    n = notify2.Notification("copiaAndroid",
                             "Ha concluido la copia de seguridad")
    n.show()
    print("\nCopia completada.")

def scan_Android():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb")
    monitor.start()

    print("Esperando conexión de dispositivo Android...")

    try:
        while True:
            device = monitor.poll(timeout=1)
            if device and device.properties.get("ACTION") == "add" and android(device):
                nombre = get_Name_Android(device)
                print(f" Dispositivo detectado: {nombre}")
                launch_Rofi(nombre)
                rutaCopia = crearCarpeta(RUTA_RESPALDO, nombre)
                crearMedia(RUTA_ANDROID, rutaCopia)

    except KeyboardInterrupt:
        print("\nSaliendo del programa.")
        exit()

if __name__ == "__main__":
    notify2.init("copiaAndroid")
    scan_Android()

