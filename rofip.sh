#!/bin/bash

nombreDispositivo=$1
mensaje=$(printf "%s\nQuieres hacer una copia de los archivos?" "$nombreDispositivo se ha conectado al equipo")

respuesta=$(echo -e "Si\nNo" | rofi -dmenu -p "$mensaje")

if [[ $respuesta == "Si" ]]; then
    exit 0

else
    exit 1

fi
