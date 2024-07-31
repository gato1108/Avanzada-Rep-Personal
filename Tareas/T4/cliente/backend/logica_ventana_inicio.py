from PyQt6.QtCore import QObject, pyqtSignal, QThread
#import parametros as p
import os
import socket


class LogicaInicio(QObject):

    senal_respuesta_validacion = pyqtSignal(bool, list)
    senal_abrir_juego = pyqtSignal(str, list)
    senal_tablero = pyqtSignal(str)
    senal_cambiar_tablero = pyqtSignal(list, str)
    senal_nombre_usuario = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def iniciar_juego(self, nombre, nivel):
        errores = []
        valid = True
        if not nombre.isalnum():
            valid = False
            errores.append('Usuario debe ser alfanumérico')
        if nombre.lower() == nombre:
            valid = False
            errores.append('Usuario debe tener una mayúscula')
        if nombre == '':
            valid = False
            errores.append('Usuario no puede ser vacío')
        if not any(i.isdigit() for i in nombre):
            valid = False
            errores.append('Usuario debe tener un número')

        ruta = os.path.join('assets', 'base_puzzles', nivel)
        tablero = []

        file = open(ruta, 'r')
        lineas = file.readlines()
        for linea in lineas:
            linea = linea.strip().split(';')
            tablero.append(linea)
        file.close()

        if valid:
            self.senal_nombre_usuario.emit(nombre)
            self.senal_abrir_juego.emit(nivel, tablero)
            self.senal_cambiar_tablero.emit(tablero, nivel)
        self.senal_respuesta_validacion.emit(valid, errores)
        
