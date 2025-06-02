#!/bin/bash

# Mostrar un diálogo con Rofi y permitir selección de "Sí" o "No"
echo -e "Sí\nNo" | rofi -dmenu -p "¿Deseas continuar?"
