import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, 
                             QHBoxLayout, QVBoxLayout)
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from os import listdir
from os.path import isfile, join
import parametros as p


class VentanaInicio(QWidget):

    senal_enviar_usuario = pyqtSignal(str, str)
    senal_enviar_nivel = pyqtSignal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, *kwargs)
        self.jugadores = []
        self.init_gui()
        self.show()

    def init_gui(self) -> None:

        self.setGeometry(50, 50, 400, 610)
        self.setWindowTitle('Ventana inicio')
        #self.setStyleSheet("background-color: lightblue;")

        #Logo
        ruta_imagen = os.path.join('assets', 'sprites', 'logo.png')
        pixeles = QPixmap(ruta_imagen)

        self.logo = QLabel(self)
        self.logo.setGeometry(100, 50, 200, 200)
        self.logo.setPixmap(pixeles)
        self.logo.setScaledContents(True)
        self.logo.setMaximumSize(200, 200)

        #Nombre usuario

        self.texto = QLabel('Ingresa tu usuario:', self)
        self.texto.setGeometry(150, 220, 200, 50)
        self.nombre = QLineEdit('', self)
        self.nombre.setGeometry(100, 255, 200, 25)

        #Barra

        ruta = os.path.join('assets', 'base_puzzles')

        archivos = [f for f in listdir(ruta) if isfile(join(ruta, f))]

        self.barra = QComboBox(self)
        for nombre in archivos:
            self.barra.addItem(nombre)
        #for i in range(1, 6):
         #   self.barra.addItem('novato_' + str(i))
          #  self.barra.addItem('intermedio_' + str(i))
           # self.barra.addItem('experto_' + str(i))
        self.barra.setGeometry(100, 300, 200, 25)

        #Botones

        self.boton_com = QPushButton("Empezar juego!", self)
        self.boton_com.setGeometry(50, 350, 150, 50)
        self.boton_com.clicked.connect(self.enviar_usuario)
        self.boton_com.clicked.connect(self.enviar_nivel)

        self.boton_sal = QPushButton("Salir :(", self)
        self.boton_sal.setGeometry(200, 350, 150, 50)
        self.boton_sal.clicked.connect(self.salir_def)

        #Laderboard

        ordenados = sorted(self.jugadores, key=lambda x: - int(x[1]))
        self.scroll = QScrollArea(self) 
        self.vbox_scroll = QVBoxLayout(self) 
        self.casa_scroll = QWidget(self)

        for usuario in ordenados:
            caja = QLabel(str(usuario[0]) + ' - ' + str(usuario[1]))
            self.vbox_scroll.addWidget(caja)

        self.casa_scroll.setLayout(self.vbox_scroll)

        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.casa_scroll)

        self.scroll.setGeometry(100, 420, 200, 150)


        self.musica = QSoundEffect(self)
        file_url = QUrl.fromLocalFile(p.MUSICA)
        self.musica.setSource(file_url)
        self.musica.setLoopCount(100)
        self.musica.play()

        self.show()

    def salir(self):
        self.musica.stop()
        self.hide()

    def salir_def(self):
        self.musica.stop()
        self.close()

    def enviar_usuario(self):
        self.senal_enviar_usuario.emit(self.nombre.text(), self.barra.currentText())

    def enviar_nivel(self):
        self.senal_enviar_nivel.emit(self.barra.currentText())

    def actualizar_scores(self):
        self.jugadores = []
        ruta = os.path.join('puntaje.txt')

        file = open(ruta, 'r')
        lineas = file.readlines()
        for linea in lineas:
            linea = linea.strip().split(',')
            self.jugadores.append(linea)
        file.close()

    def recibir_validacion(self, valid, errores):
        if valid:
            self.hide()
        else:
            self.nombre.setPlaceholderText('')
            text_errores = ' '.join(errores)
            self.nombre.setPlaceholderText(text_errores)
            self.nombre.setText("")

    def actualizar_score(self, score, usuario):
        f = open("puntaje.txt", "a")
        f.write('\n' + usuario + ',' + str(score) + '\n')
        f.close()

    def aparecer(self):
        self.actualizar_scores()
        self.show()

class VentanaFin(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, *kwargs)
        self.jugadores = []

    def init_gui(self, gano) -> None:


        self.setGeometry(30, 30, 200, 200)
        self.setWindowTitle('Ventana fin')
        #self.setStyleSheet("background-color: lightblue;")
        self.mus_fin = QSoundEffect(self)
        if gano:
            self.texto = QLabel('Ganaste!', self)
            file_url = QUrl.fromLocalFile(p.GANAR)
        else:
            self.texto = QLabel('Se acabó el tiempo:()', self)
            file_url = QUrl.fromLocalFile(p.PERDER)
        self.texto.setGeometry(0, 0, 150, 150)

        self.mus_fin.setSource(file_url)
        self.mus_fin.play()

        self.show()


if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaInicio()
    sys.exit(app.exec())