#---------------------------SERVIDOR---------------------------

import socket
from threading import Thread
import sys
from enc_dec import encode, decode
import os
import json

PORT =  int(sys.argv[1])
#CAMBIAR
f = open('conexion_servidor.json')
data = json.load(f)
HOST = data["host"]
f.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()

def escuchar_cliente(socket_cliente: socket.socket) -> None:
    while True:
        try:
            mensaje = decode(socket_cliente.recv(4096))
            nivel = mensaje[1]
            ruta = os.path.join('assets', 'solucion_puzzles', nivel)

            respuesta = ''
            for linea in mensaje[0]:
                a = ''
                for car in linea:
                    a += str(car)
                respuesta += a
            file = open(ruta, 'r')
            lineas = file.readlines()
            
            solucion = ''
            for linea in lineas:
                linea = linea.strip()
                solucion += linea

            file.close()
            if respuesta == solucion:
                socket_cliente.send(encode('CORRECTO'))
            else:
                socket_cliente.send(encode('MAL'))

        except Exception:
            return

if __name__ == "__main__":
    while True:
        try:
            print("Esperando que alguien se quiera conectar...")
            # Aceptamos a un cliente
            socket_cliente, address = sock.accept()
            print("Conexión aceptada desde", address)

            # Creamos un thread encargado de escuchar a ese cliente
            thread = Thread(target=escuchar_cliente,
                            args=(socket_cliente,), daemon=True)
            thread.start()
        except ConnectionError:
            print("Ocurrió un error.")