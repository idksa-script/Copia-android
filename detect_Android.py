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

def launch_Rofi():
    subprocess.run(["./hola.sh"])

def scan_Android():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb")
    monitor.start


    
    for action, device in monitor:
        if action == "add" and android(device):
            print(get_Name_Android(device))
            launch_Rofi()


          

if __name__ == "__main__":
    scan_Android()
