import dcciudad 
import os
import copy

class RedMetro:
    def __init__(self, red: list, estaciones: list) -> None:
        self.red = red
        self.estaciones = estaciones

    #retorna lista con red y número de estaciones.
    def informacion_red(self) -> list: #TA OK
        numero_estaciones = len(self.estaciones)
        tuneles_salen = []

        for fila in self.red:
            tuneles_salen.append(sum(fila)) 

        return [numero_estaciones, tuneles_salen]

    #Agregar tunel entre 2 estaciones
    def agregar_tunel(self, inicio: str, destino: str) -> int: #TA OK
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)

        if self.red[ind_inicio][ind_destino] == 1:
            return -1
        self.red[ind_inicio][ind_destino] = 1

        return sum(self.red[ind_inicio])

    #quitar tunel entre 2 estaciones
    def tapar_tunel(self, inicio: str, destino: str) -> int: #TA OK
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)

        if self.red[ind_inicio][ind_destino] == 0:
            return -1
        self.red[ind_inicio][ind_destino] = 0

        return sum(self.red[ind_inicio])
    
    #invertir dirección de túnel
    def invertir_tunel(self, estacion_1: str, estacion_2: str) -> bool: #TA OK
        ind_1 = self.estaciones.index(estacion_1)
        ind_2 = self.estaciones.index(estacion_2)
        direccion_ida = self.red[ind_1][ind_2]
        direccion_vueta = self.red[ind_2][ind_1]

        if direccion_ida == 1 and direccion_vueta == 1:
            return True
        elif direccion_ida == 1 and direccion_vueta == 0:
            self.red[ind_1][ind_2] = 0
            self.red[ind_2][ind_1] = 1
            return True
        elif direccion_ida == 0 and direccion_vueta == 1:
            self.red[ind_1][ind_2] = 1
            self.red[ind_2][ind_1] = 0
            return True
        else:
            return False

    #Retorna si existe ruta entre 2 estaciones, y si esta se encuenra a 0, 1 o más estaciones intermedias.
    def nivel_conexiones(self, inicio: str, destino: str) -> str:
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)
        alcanzable = dcciudad.alcanzable(self.red,ind_inicio,ind_destino)
        cuadrado = dcciudad.elevar_matriz(self.red, 2)

        if not alcanzable:
            return "no hay ruta"
        elif self.red[ind_inicio][ind_destino] == 1:
            return "túnel directo"
        elif cuadrado[ind_inicio][ind_destino] > 0:
            return "estación intermedia"
        return "muy lejos"

    # Retorna la cantidad de rutas posible entre 2 estaciones, viajando una distancia de estaciones fija.
    def rutas_posibles(self, inicio: str, destino: str, p_intermedias: int) -> int:
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)
        potencia = dcciudad.elevar_matriz(self.red, p_intermedias+1)

        return potencia[ind_inicio][ind_destino]

    #Retorna la longitud del ciclo más corto y -1 si es que no existe ciclo
    def ciclo_mas_corto(self, estacion: str) -> int:
        ind_estacion = self.estaciones.index(estacion)
        N = len(self.estaciones)

        for num_pot in range(1,N+1):
            potencia = dcciudad.elevar_matriz(self.red, num_pot)
            if potencia[ind_estacion][ind_estacion] > 0:
                return num_pot-1
        return -1

    #Retorna lista con estaciones intermedias (y adyacentes) a 2 estaciones
    def estaciones_intermedias(self, inicio: str, destino: str) -> list:
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)
        intermedias = []
        for estacion in self.estaciones:
            ind_estacion = self.estaciones.index(estacion)
            distinto_inicio_destino = (not estacion == inicio and not estacion == destino)
            conexion_inicio = (self.red[ind_inicio][ind_estacion] == 1)
            conexio_destino = (self.red[ind_estacion][ind_destino] == 1)
            if distinto_inicio_destino and conexio_destino and conexion_inicio:
                intermedias.append(estacion)
        return intermedias

    #Retorna lista de pares de estaciones intermedias (y adyacentes) a 2 estaciones
    def estaciones_intermedias_avanzado(self, inicio: str, destino: str) -> list:
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)
        intermedias = []
        for estacion_1 in self.estaciones:
            for estacion_2 in self.estaciones:
                ind_estacion_1 = self.estaciones.index(estacion_1)
                ind_estacion_2 = self.estaciones.index(estacion_2)
                conexion_1 = (self.red[ind_inicio][ind_estacion_1] == 1)
                conexion_2 = (self.red[ind_estacion_1][ind_estacion_2] == 1)
                conexion_3 = (self.red[ind_estacion_2][ind_destino] == 1)
                if conexion_1 and conexion_2 and conexion_3:
                    intermedias.append([estacion_1,estacion_2])
        return intermedias

    #Lee un archivo y actualiza una red a partir de el
    def cambiar_planos(self, nombre_archivo: str) -> bool:
        nombre = 'data/'+nombre_archivo
        if not os.path.exists(nombre):
            return False
        with open(nombre,'rt') as archivo:
            lineas = archivo.readlines()
        texto = []
        for linea in lineas:
            texto.append(linea.strip())
        N_nuevo = int(texto[0])
        estaciones_nuevas = texto[1: N_nuevo+1]
        red_nueva = []
        red_en_lista = texto[-1].split(',')
        red_en_lista_int = [int(i) for i in red_en_lista]
        for num in range(N_nuevo):
            red_nueva.append(red_en_lista_int[num*N_nuevo: (num+1)*N_nuevo])
        self.red = red_nueva
        self.estaciones = estaciones_nuevas
        return True
    
    #Cantidad mínima de paradas intermedias (-1 si no se puede)
    def minima_distancia(self, inicio, destino, red_nueva):
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)
        red_copia = copy.deepcopy(self.red)
        self.red = red_nueva
        N = len(self.estaciones)
        for exponente in range(1,N+1):
            potencia = dcciudad.elevar_matriz(self.red, exponente)
            if potencia[ind_inicio][ind_destino] > 0:
                self.red = red_copia
                return exponente-1
        self.red = red_copia
        return -1
    
    #Retorna red con unos cambiado por número binario
    def cambiar_por_binario(self, binario):
        red_nueva = copy.deepcopy(self.red)
        N = len(self.estaciones)
        contador = 0
        for fila in range(N):
            for columna in range(N):
                if self.red[fila][columna] == 1:
                    red_nueva[fila][columna] = int(binario[contador])
                    contador += 1
        return red_nueva
    
    #retorna todos los posibles strings binarios de largo c
    def numeros_binarios(self):
        caminos = 0
        for fila in self.red:
            caminos += sum(fila)
        num = ['0', '1']
        for linea in range(caminos-1):
            ceros = []
            unos = []
            for elemento in num:
                ceros.append(str(0) + elemento)
                unos.append(str(1) + elemento)
            num = ceros + unos
        return num

    #Retorna lista con todos los subgrafos de red
    def subgrafos(self):
        caminos = 0
        sub = []
        numeros = self.numeros_binarios()
        for fila in self.red:
            caminos += sum(fila)
        for combinacion in numeros:
            sub.append(self.cambiar_por_binario(combinacion))
        return sub

    #Encuentra una sub-red que garantiza una distancia mínima entre 2 estaciones
    def asegurar_ruta(self, inicio: str, destino: str, p_intermedias: int) -> list:
        sub = self.subgrafos()
        ind_inicio = self.estaciones.index(inicio)
        ind_destino = self.estaciones.index(destino)
        redes_nuevas = []
        for subgrafo in sub:
            if self.minima_distancia(inicio, destino, subgrafo) == p_intermedias:
                redes_nuevas.append(subgrafo)
        if len(redes_nuevas) > 0:
            return redes_nuevas[0]
        return redes_nuevas