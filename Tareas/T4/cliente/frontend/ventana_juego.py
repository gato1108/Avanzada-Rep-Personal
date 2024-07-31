import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout)
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QScrollArea, QGridLayout 
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, QTimer, QThread
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
import parametros as p
from time import sleep
from PyQt6.QtCore import QUrl


class Sandia(QLabel):

    senal_apretar_sandia = pyqtSignal()

    def __init__(self, parent=None ,*args, **kwargs):
        super(Sandia, self).__init__(parent)

    def mover(self, new_x, new_y):
        self.move(new_x, new_y)

    def aparecer(self):
        pass
        #self.setPixmap(QPixmap(p.SANDIA))

    def esconder(self):
        pass
    
    def mousePressEvent(self, ev):
        if self.underMouse():
            self.senal_apretar_sandia.emit()
            self.media_player_wav = QSoundEffect(self)
            self.media_player_wav.setVolume(0.5) 
            file_url = QUrl.fromLocalFile(p.CLICK_SANDIA)
            self.media_player_wav.setSource(file_url)
            self.media_player_wav.play()

            self.hide()
        
        #self.clicked.emit()


class MiThread(QThread):

    senal_aparecer_lechuga = pyqtSignal(int, int)

    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        sleep(p.TIEMPO_TRANSICION)
        #self.senal_aparecer_lechuga.emit(self.x, self.y)

class VentanaJuego(QWidget):

    senal_iniciar_juego = pyqtSignal()
    senal_tecla = pyqtSignal(str)
    senal_mandar_comando = pyqtSignal(list)
    senal_fin = pyqtSignal(float)
    senal_gano = pyqtSignal(float, str)
    senal_volver_inicio = pyqtSignal()
    senal_acabar = pyqtSignal(bool)

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, *kwargs)
        self.tablero = []
        #self.qlabel_tablero = []
        self.casillas = {}
        self.tiempo = 40
        self.boton_comprobar = ''
        self.pepa = ''
        self.puntaje = 0
        self.usuario = 'Nombre_usuario'
        self.sandias = Sandia(self)
        self.timer_casillas = {}
        #self.mensajes = QLabel('HOLA')
        #self.show()

    def mostrar(self, nivel, tablero) -> None:

        self.setGeometry(50, 50, 1000, 610)
        self.setWindowTitle('Ventana juego')

        self.boton_sal = QPushButton("SALIR", self)
        self.boton_sal.setGeometry(800, 550, 150, 20)
        self.boton_sal.clicked.connect(self.salir)

        self.boton_pausa = QPushButton("PAUSAR", self)
        self.boton_pausa.setGeometry(800, 450, 150, 20)

        self.boton_comprobar = QPushButton("COMPROBAR", self)
        self.boton_comprobar.clicked.connect(self.enviar)
        self.boton_comprobar.setGeometry(800, 350, 150, 20)

        self.tiempo_text = QLabel('TIEMPO: ' + str(self.tiempo), self)
        self.tiempo_text.setGeometry(800, 250, 150, 20)

        self.mensajes = QLabel('GOOD LUCK!', self)
        self.mensajes.setGeometry(800, 150, 150, 20)

        self.dim_tablero_x = len(tablero[1])
        dim_tablero_y = len(tablero[0])

        for i in range(1, 1 + self.dim_tablero_x):
            texto = QLabel(tablero[0][i-1], self)
            texto.setFixedSize(20, 20)
            texto.setGeometry(60 + 25 * i, 60, 20, 20)

        for i in range(1, 1 + dim_tablero_y):
            texto = QLabel(tablero[1][i-1], self)
            texto.setFixedSize(20, 20)
            texto.setGeometry(60, 60 + 25 * i, 20, 20)

        for i in range(dim_tablero_y):
            for j in range(self.dim_tablero_x):
                frontal = QLabel(self)
                frontal.setFixedSize(20, 20)
                frontal.setGeometry(85 + 25 * j, 85 + 25 * i, 20, 20)
                frontal.setStyleSheet("background-color:green")
                pixmap = QPixmap(p.LECHUGA)
                pixmap.scaledToWidth(20)
                frontal.setPixmap(pixmap)
                self.casillas[(i, j)] = frontal
                self.timer_casillas[(i, j)] = QTimer()

        pixmap_pepa = QPixmap(p.D_0)
        pixmap_pepa.scaledToWidth(20)

        self.casa_pepa = QLabel(self)
        self.casa_pepa.setFixedSize(20, 20)
        self.casa_pepa.setGeometry(85, 85, 20, 20)
        self.casa_pepa.setPixmap(pixmap_pepa)

        self.sandias = Sandia(self)
        self.sandias.setGeometry(0, 0, 50, 50)
        self.sandias.setFixedSize(50, 50)

        self.show()

    def set_nombre(self, nombre):
        self.usuario = nombre

    def salir(self):
        self.close()

    def pausar(self):
        #Esconder tablero
        pass
        #Parar tiempo

    def enviar(self):
        self.senal_mandar_comando.emit(self.tablero)

    def aparecer_lechuga(self, x, y):
        pixmap = QPixmap(p.LECHUGA)
        self.casillas[(x, y)].setPixmap(pixmap)
        self.casillas[(x, y)].setStyleSheet("background-color:green")

    def actualizar_tablero(self, se_mueve, dir, pos_x, pos_y, tablero):
        x_0 = self.casa_pepa.x()
        y_0 = self.casa_pepa.y()

        #animar movimiento
        if se_mueve and not dir.lower() == 'g':
            #pixmap = QPixmap(p.D_0)
            #self.casillas[(pos_x, pos_y)][0].setPixmap(pixmap)
            if dir.lower() == 'd':
                self.casa_pepa.move(x_0, y_0 + 25)
                self.casa_pepa.setPixmap(QPixmap(p.D_0))
            if dir.lower() == 's':
                self.casa_pepa.move(x_0 + 25, y_0)
                self.casa_pepa.setPixmap(QPixmap(p.R_0))
            if dir.lower() == 'a':
                self.casa_pepa.move(x_0, y_0 - 25)
                self.casa_pepa.setPixmap(QPixmap(p.U_0))
            #    self.casillas[(pos_x - 1, pos_y)][0].setPixmap(QPixmap('vacio.png'))
            if dir.lower() == 'w':
                self.casa_pepa.move(x_0 - 25, y_0)
                self.casa_pepa.setPixmap(QPixmap(p.L_0))
              #  self.casillas[(pos_x, pos_y + 1)][0].setPixmap(QPixmap('vacio.png'))

        
        elif dir.lower() == 'g':
            #LIMPIAR CASILLA
            if tablero[pos_x][pos_y] == 0:
                self.casillas[(pos_x, pos_y)].setStyleSheet("background-color:white")
                self.casillas[(pos_x, pos_y)].setPixmap(QPixmap('vacio.png'))

                self.media_player_wav = QSoundEffect(self)
                self.media_player_wav.setVolume(1) 
                file_url = QUrl.fromLocalFile(p.COMER)
                self.media_player_wav.setSource(file_url)
                self.media_player_wav.play()
                #self.casillas[(pos_x, pos_y)][1].setPixmap(QPixmap('vacio.png'))
                #ruta = os.path.join('assets', 'sprites', 'poop.png')
                #self.casillas[(pos_x, pos_y)][1].swap(QPixmap(ruta))

            #LLENAR CASILLA
            else:
                pixmap = QPixmap(p.POOP)
                pixmap.scaledToWidth(20)
                self.casillas[(pos_x, pos_y)].setPixmap(pixmap)
                self.media_player_wav = QSoundEffect(self)
                self.media_player_wav.setVolume(1) 
                file_url = QUrl.fromLocalFile(p.POOP_AUDIO)
                self.media_player_wav.setSource(file_url)
                self.media_player_wav.play()

                self.aparecer_lechuga(pos_x, pos_y)

                #self.timer_casillas[(pos_x, pos_y)] = QTimer()
                ##self.timer_casillas[(pos_x, pos_y)].setSingleShot(True)
                #self.timer_casillas[(pos_x, pos_y)].start(p.TIEMPO_TRANSICION * 1000)
                #self.timer_casillas[(pos_x, pos_y)].timeout.connect(self.aparecer_lechuga(pos_x, pos_y))

                #thread = MiThread()
                #thread.start()

                #self.casillas[(pos_x, pos_y)].setStyleSheet("background-color:green")
                #pixmap = QPixmap(p.LECHUGA)
                #pixmap.scaledToWidth(20)
                #self.casillas[(pos_x, pos_y)].setPixmap(pixmap)

                #poop = os.path.join('assets', 'sprites', 'poop.png')
                #self.casillas[(pos_x, pos_y)][1].setPixmap(QPixmap(poop))
                #TEMPORIZADOR PARA CAMBIAR A LECHUGA
    

    def actualizar_tiempo(self, tiempo_restante, tiempo_usado):
        self.tiempo = tiempo_restante
        n = self.dim_tablero_x
        self.puntaje = round(tiempo_restante * n * n * p.CONSTANTE / (tiempo_usado), 2)
        self.tiempo_text.setText('TIEMPO: ' + str(tiempo_restante))
        if self.tiempo < 1:
            #self.senal_fin.emit(self.puntaje)
            self.senal_volver_inicio.emit()
            self.senal_fin.emit(False)
            self.close()
            #self.tiempo_text.setText('Se acabó el tiempo :(')
    
    def update_label(self, mensaje):
        self.mensajes.setText(str(mensaje))
        if mensaje == 'CORRECTO':
            self.mensajes.setText('Solución Correcta!')

            self.senal_gano.emit(self.puntaje, self.usuario)
            self.senal_volver_inicio.emit()
            self.senal_fin.emit(True)

            self.close()

        elif mensaje == 'MAL':
            self.mensajes.setText('Solución Incorrecta')

    def keyPressEvent(self, event):
        if event.text().lower() == 'w':
            self.senal_tecla.emit('A')
        elif event.text().lower() == 's':
            self.senal_tecla.emit('D')
        elif event.text().lower() == 'a':
            self.senal_tecla.emit('W')
        elif event.text().lower() == 'd':
            self.senal_tecla.emit('S')
        elif event.text().lower() == 'g':
            self.senal_tecla.emit('G')

    def mostrar_sandia(self, new_x, new_y):
        self.sandias.show()
        self.sandias.move(new_x, new_y)
        self.sandias.setPixmap(QPixmap(p.SANDIA))





if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaJuego()
    sys.exit(app.exec())