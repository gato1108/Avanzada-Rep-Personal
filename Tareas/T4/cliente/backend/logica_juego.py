from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QThread
import socket
import os
import parametros as p
from random import randint
from enc_dec import encode, decode 

class EscucharThread(QThread):
    senal_mensaje_del_servidor = pyqtSignal(str)

    def __init__(self, socket: socket.socket) -> None:
        super().__init__()
        self.socket = socket

    def run(self) -> None:
        print("Levantando el thread que escucha al servidor...")
        while True:
            data = decode(self.socket.recv(4096))
            self.senal_mensaje_del_servidor.emit(data)

class LogicaJuego(QObject):

    senal_tablero = pyqtSignal(list)
    senal_se_mueve = pyqtSignal(bool, str, int, int, list)
    actualizar_tablero = pyqtSignal(list)
    senal_tiempo = pyqtSignal(int, int)
    senal_aparecer_sandia = pyqtSignal(int, int)
    senal_update_label = pyqtSignal(str)
    #senal_mensaje_del_servidor = pyqtSignal(int)

    def __init__(self, host, port):
        super().__init__()
        self.nivel = 'novato_1'
        self.tablero = []
        self.pos_pepa_x = 0
        self.pos_pepa_y = 0
        self.max_x = 110
        self.max_y = 110
        self.tiempo_restante = p.TIEMPO_JUEGO
        self.timers = []
        self.puntaje = 0
        self.tiempo_usado = 0

        self.thread = None

        print("Inicializando cliente...")
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

        try:
            self.conectar_a_servidor()
            self.escuchar()
        except ConnectionError:
            print("Conexión terminada.")
            self.socket_cliente.close()
            exit()

    def conectar_a_servidor(self) -> None:
        self.socket_cliente.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor.")

    def escuchar(self) -> None:
        if self.thread is None or not self.thread.isRunning():
            self.thread = EscucharThread(self.socket_cliente)
            self.thread.senal_mensaje_del_servidor.connect(self.procesar_mensaje)
            self.thread.start()

    def procesar_mensaje(self, mensaje):
        self.senal_update_label.emit(mensaje)

    def mandar_comando(self, comando):
        self.socket_cliente.send(encode([self.tablero, self.nivel]))

    def set_tablero(self, tablero, nivel):
        self.nivel = nivel
        self.pos_pepa_x = 0
        self.pos_pepa_y = 0
        self.instanciar_timer()
        self.tiempo_sandias()
        self.max_x = len(tablero[0])
        self.max_y = len(tablero[1])
        for i in range(self.max_y):
            fila = []
            for j in range(self.max_x):
                fila.append(1)
            self.tablero.append(fila)

    def mover_pepa(self, mov):
        se_mueve = False
        if mov.upper() == 'A' and self.pos_pepa_x > 0:
            self.pos_pepa_x -= 1
            se_mueve = True
        if mov.upper() == 'D' and self.pos_pepa_x < self.max_x - 1:
            self.pos_pepa_x += 1
            se_mueve = True
        if mov.upper() == 'W' and self.pos_pepa_y > 0:
            self.pos_pepa_y -= 1
            se_mueve = True
        if mov.upper() == 'S' and self.pos_pepa_y < self.max_y - 1:
            self.pos_pepa_y += 1
            se_mueve = True
        if mov.upper() == 'G':
            if self.tablero[self.pos_pepa_x][self.pos_pepa_y] == 1:
                self.tablero[self.pos_pepa_x][self.pos_pepa_y] = 0
            else:
                self.tablero[self.pos_pepa_x][self.pos_pepa_y] = 1
        self.senal_se_mueve.emit(se_mueve, mov, self.pos_pepa_x, self.pos_pepa_y, self.tablero)
        #if se_mueve:
         #   self.actualizar_tablero.emit(self.tablero)

    def tiempo_sandias(self):
        self.temporizador_sandias = QTimer(self)
        self.temporizador_sandias.start(1000 * p.TIEMPO_APARICION)
        self.temporizador_sandias.timeout.connect(self.aparecer_sandia)

    def aparecer_sandia(self):
        pos_x = randint(0, p.MAX_SAN_X)
        pos_y = randint(0, p.MAX_SAN_Y)
        #if self.tiempo_restante > 0:
        self.senal_aparecer_sandia.emit(pos_x, pos_y)

    
    def instanciar_timer(self):
        self.tiempo_restante = p.TIEMPO_JUEGO

        self.temporizador = QTimer(self)
        self.temporizador.start(1000)
        self.temporizador.timeout.connect(self.actualizar_tiempo)
        #self.timers.append(self.temporizador)

    def recolectar_sandia(self):
        self.tiempo_restante += p.TIEMPO_ADICIONAL
        #tiempo_juego = self.temporizador.remainingTime() // 1000
        self.senal_tiempo.emit(round(self.tiempo_restante), self.tiempo_usado)

    def actualizar_tiempo(self):
        self.tiempo_usado += 1
        self.tiempo_restante -= 1
        #tiempo_juego = self.temporizador.remainingTime() // 1000
        self.senal_tiempo.emit(round(self.tiempo_restante), self.tiempo_usado)
        #return self.tiempo_restante
