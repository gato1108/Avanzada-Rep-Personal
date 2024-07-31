#---------------------------CLIENTE---------------------------

from PyQt6.QtWidgets import QApplication
import sys

from backend.logica_ventana_inicio import LogicaInicio
from backend.logica_juego import LogicaJuego
from frontend.ventana_inicio import VentanaInicio, VentanaFin
from frontend.ventana_juego import VentanaJuego

import json
#rom frontend.ventana_fin import VentanaFin

PORT =  int(sys.argv[1])
f = open('conexion_cliente.json')
data = json.load(f)
HOST = data["host"]
f.close()

if __name__ == "__main__":
    # Hook para imprimir errores
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication(sys.argv)

    # Usamos nuestras constantes
    host = HOST
    port = PORT

    # Instanciamos nuestro backend y frontend
    #back = backend.Logica(host, port)
    #frontend = ventana.MainWindow()

    ventana_inicio = VentanaInicio()
    ventana_juego = VentanaJuego()
    logica_inicio = LogicaInicio()
    #ventana_fin = VentanaFin()

    # Conectamos señales
    ventana_inicio.senal_enviar_usuario.connect(logica_inicio.iniciar_juego)
    logica_inicio.senal_nombre_usuario.connect(ventana_juego.set_nombre)

    logica_inicio.senal_respuesta_validacion.connect(ventana_inicio.recibir_validacion)
    logica_inicio.senal_abrir_juego.connect(ventana_juego.mostrar)

    logica_juego = LogicaJuego(host, port)
    ventana_fin = VentanaFin()
    logica_inicio.senal_cambiar_tablero.connect(logica_juego.set_tablero)
    logica_juego.senal_update_label.connect(ventana_juego.update_label)
    ventana_juego.senal_mandar_comando.connect(logica_juego.mandar_comando)


    ventana_juego.senal_tecla.connect(logica_juego.mover_pepa)
    logica_juego.senal_se_mueve.connect(ventana_juego.actualizar_tablero)
    logica_juego.senal_tiempo.connect(ventana_juego.actualizar_tiempo)
    logica_juego.senal_aparecer_sandia.connect(ventana_juego.mostrar_sandia)
    ventana_juego.sandias.senal_apretar_sandia.connect(logica_juego.recolectar_sandia)

    ventana_juego.senal_gano.connect(ventana_inicio.actualizar_score)
    ventana_juego.senal_fin.connect(ventana_fin.init_gui)
    ventana_juego.senal_volver_inicio.connect(ventana_inicio.aparecer)
    

    #ventana_juego.senal_fin.connect(ventana_fin.init_gui)

    #ventana_fin.senal_puntaje.connect(ventana_inicio.init_gui)

    # Mostramos la ventana y ejecutamos pyqt
    ventana_inicio.show()
    sys.exit(app.exec())