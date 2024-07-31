from typing import List
from clases import Tortuga
import pickle


###################
#### ENCRIPTAR ####
###################
def serializar_tortuga(tortuga: Tortuga) -> bytearray:
    try:
        tortuga_ser = pickle.dumps(tortuga)
        return bytearray(tortuga_ser)
    except AttributeError as error:
        raise ValueError()

def verificar_rango(mensaje: bytearray, inicio: int, fin: int) -> None:
    if inicio > fin:
        raise AttributeError()
    elif len(mensaje) < fin:
        raise AttributeError()
    elif inicio < 0:
        raise AttributeError()
    return None


def codificar_rango(inicio: int, fin: int) -> bytearray:
    pos = bytearray()
    inicio_ser = int.to_bytes(inicio, 3, byteorder= 'big')
    fin_ser = int.to_bytes(fin, 3, byteorder= 'big')
    pos.extend(inicio_ser)
    pos.extend(fin_ser)
    return pos

test = codificar_rango(1, 3)
print(test)


def codificar_largo(largo: int) -> bytearray:
    return bytearray((largo).to_bytes(3, 'big'))


def separar_msg(mensaje: bytearray, inicio: int, fin: int) -> List[bytearray]:
    m_extraido = mensaje[inicio: fin + 1]
    if len(m_extraido)%2 == 1:
        m_extraido = m_extraido[::-1]
    for i in range(inicio, fin + 1):
        mensaje[i] = i-inicio
    return [m_extraido, mensaje]


def encriptar(mensaje: bytearray, inicio: int, fin: int) -> bytearray:
    # No modificar
    verificar_rango(mensaje, inicio, fin)

    m_extraido, m_con_mascara = separar_msg(mensaje, inicio, fin)
    rango_codificado = codificar_rango(inicio, fin)
    return (
        codificar_largo(fin - inicio + 1)
        + m_extraido
        + m_con_mascara
        + rango_codificado
    )


######################
#### DESENCRIPTAR ####
######################
def deserializar_tortuga(mensaje_codificado: bytearray) -> Tortuga:
    try:
        men = pickle.loads(mensaje_codificado)
        return men
    except ValueError as error:
        raise AttributeError()


def decodificar_largo(mensaje: bytearray) -> int:
    return int.from_bytes(mensaje[0: 3], byteorder='big')


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    largo = decodificar_largo(mensaje)
    inicio = int.from_bytes(mensaje[-6: -3], byteorder='big')
    fin = int.from_bytes(mensaje[-3:], byteorder='big')

    m_bytes_rango = mensaje[3: largo + 3]
    if len(m_bytes_rango)%2 == 1:
         m_bytes_rango = m_bytes_rango[::-1]
    m_con_mascara = mensaje[largo + 3:-6]
    rango_codificado = mensaje[-6:]

    return [m_bytes_rango, m_con_mascara, rango_codificado]


def decodificar_rango(rango_codificado: bytearray) -> List[int]:
    inicio = int.from_bytes(rango_codificado[0: 3], byteorder='big')
    fin = int.from_bytes(rango_codificado[3: 6], byteorder='big')
    return [inicio, fin]


def desencriptar(mensaje: bytearray) -> bytearray:
    lista = separar_msg_encriptado(mensaje)
    inicio = int.from_bytes(mensaje[-6: -3], byteorder='big')
    fin = int.from_bytes(mensaje[-3:], byteorder='big')
    m_con_mascara = lista[1]
    m_con_mascara[inicio: fin + 1] = lista[0]
    return m_con_mascara

if __name__ == "__main__":
    # Tortuga
    tama = Tortuga("Tama2")
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
    print(tama.celebrar_anivesario())
    print()

    # Encriptar
    original = serializar_tortuga(tama)
    print("Original: ", original)
    encriptado = encriptar(original, 6, 24)
    print("Encriptado: ", encriptado)
    print()

    # Desencriptar
    mensaje =  bytearray(b'\x00\x00\x13roT\x07\x8c\x94sesalc\x06\x8c\x00\x00\x00\x00\x00\x80\x04\x958\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12tuga\x94\x93\x94)\x81\x94}\x94(\x8c\x06nombre\x94\x8c\x05Tama2\x94\x8c\x04edad\x94K\x01ub.\x00\x00\x06\x00\x00\x18')
    desencriptado = desencriptar(mensaje)
    tama = deserializar_tortuga(desencriptado)

    # Tortuga
    print("Tortuga: ", tama)
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
