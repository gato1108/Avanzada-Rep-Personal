from copy import copy
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator

from parametros import RUTA_PELICULAS, RUTA_GENEROS
from utilidades import (
    Pelicula, Genero, obtener_unicos, imprimir_peliculas,
    imprimir_generos, imprimir_peliculas_genero, imprimir_dccmax
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_peliculas(ruta: str) -> Generator:

    f = open(ruta, "r")
    r = f.readlines()
    for linea in r:
        contenido = linea.strip('\n').split(',')
        if not contenido[0] == 'id':
            pel = Pelicula(int(contenido[0]), contenido[1], contenido[2], int(contenido[3]), float(contenido[4]))
            yield pel


def cargar_generos(ruta: str) -> Generator:
    f = open(ruta, "r")
    r = f.readlines()
    for linea in r:
        contenido = linea.strip('\n').split(',')
        if not contenido[0] == 'genero':
            pel = Genero(contenido[0], int(contenido[1]))
            yield pel


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_directores(generador_peliculas: Generator) -> set:
    mapeo = map(lambda x: x[2], generador_peliculas)
    return obtener_unicos(mapeo)


def obtener_str_titulos(generador_peliculas: Generator) -> str:
    mapeo = map(lambda x: x[1], generador_peliculas)
    return reduce(lambda x, y: str(x) + ', ' + str(y), mapeo, '')[2:]


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None
) -> filter:
    
    if not director == None:
        generador_peliculas =  filter(lambda x: x[2] == director, generador_peliculas)

    if not rating_min == None:
        generador_peliculas = filter(lambda x: x[4] >= rating_min, generador_peliculas)

    if not rating_max == None:
        generador_peliculas = filter(lambda x: x[4] <= rating_max, generador_peliculas)

    return generador_peliculas


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None
) -> Generator:
    gen = product(generador_peliculas, generador_generos)
    fil = filter(lambda x: int(x[0][0]) == int(x[1][1]) , gen)
    if not genero == None:
        fil = filter(lambda x: x[1][0] == genero , fil)
    return fil


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class DCCMax:
    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:
    def __init__(self, iterable_peliculas: list) -> None:
        self.peliculas = copy(iterable_peliculas)

    def __iter__(self):
        self.peliculas.sort(key = lambda x: [int(x[3]), -float(x[4])])
        return self

    def __next__(self) -> tuple:
        if not self.peliculas:
            raise StopIteration()
        else:
            valor = self.peliculas.pop(0)
            return valor


if __name__ == '__main__':
    print('> Cargar películas:')
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print('> Cargar géneros')
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print('> Obtener directores:')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print('> Obtener string títulos')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print('> Filtrar películas (por director):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(
        generador_peliculas, director='Christopher Nolan'
    ))
    print('\n> Filtrar películas (rating min):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print('\n> Filtrar películas (rating max):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print('> Filtrar películas por género')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, 'Biography'
    ))
    print()

    print('> DCC Max...')
    imprimir_dccmax(DCCMax(list(cargar_peliculas(RUTA_PELICULAS))))