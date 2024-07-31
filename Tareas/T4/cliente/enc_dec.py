import pickle

def encode(mensaje):
    mensaje_enc = bytearray()
    dump = pickle.dumps(mensaje)

    #Primeros 4 bytes
    largo = len(dump)
    largo_enc = int.to_bytes(largo, 4, byteorder= 'big')
    mensaje_enc.extend(largo_enc)

    bloques = (largo - 1) // 25 + 1
    block = 0
    for block in range(0, bloques):
        num_block = int.to_bytes(block, 3, byteorder= 'big')
        mensaje_enc.extend(num_block)

        if block == bloques - 1:
            restante = 25 - ((largo - 1) % 25 + 1)
            pos_inicio = 25 * block 
            mensaje_enc.extend(dump[pos_inicio: ])
            for i in range(restante):
                mensaje_enc.extend(b'\x00')
        else:
            pos_inicio = 25 * block 
            pos_fin = 25 * block + 25
            mensaje_enc.extend(dump[pos_inicio: pos_fin])

    return mensaje_enc

def decode(mensaje):
    largo = int.from_bytes(mensaje[0: 4], byteorder='big')
    restante = 25 - ((largo - 1) % 25 + 1)

    mensaje = mensaje[4: ]
    mensaje = mensaje[: -restante]

    bytes_limpios = bytearray()

    for i in range(len(mensaje)):
        if i % 28 > 2:
            bytes_limpios.append(mensaje[i])

    return pickle.loads(bytes_limpios)