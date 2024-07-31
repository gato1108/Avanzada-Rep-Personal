import Clases_cambio_atacar as cl 

def instanciar_oponente(contenido):
    seguir0 = 1
    contenido = contenido.replace('\n',';')
    contenido = contenido.split(';')
    contenido = [gato.split(',') for gato in contenido]

    gatos = []

    for gato in contenido:
        if len(gato) != 7:
            print(f'ERROR: Dato inválido: {gato[0]} en longitud')
            seguir0 = 0
        elif not (gato[2].isnumeric() and gato[3].isnumeric() and gato[4].isnumeric() and gato[5].isnumeric() and gato[6].isnumeric()):
            print(f'ERROR: Dato inválido: {gato[0]} en númerico')
            seguir0 = 0
        elif not (gato[1] in ['MAG', 'CAB', 'GUE', 'CAR', 'PAL','MDB']):
            print(f'ERROR: Dato inválido: {gato[0]} en clase')
            seguir0 = 0
        else:
            if gato[1] == 'MAG':
                gatos.append(cl.Mago(gato[0], int(gato[2]), int(gato[2]),int(gato[3]), int(gato[4]), int(gato[5]), int(gato[6])))
            elif gato[1] == 'CAB':
                gatos.append(cl.Caballero(gato[0], int(gato[2]), int(gato[2]),int(gato[3]), int(gato[4]), int(gato[5]), int(gato[6])))
            elif gato[1] == 'GUE':
                gatos.append(cl.Guerrero(gato[0], int(gato[2]), int(gato[2]),int(gato[3]), int(gato[4]), int(gato[5]), int(gato[6])))
            elif gato[1] == 'CAR':
                gatos.append(cl.CaballeroArcano(gato[0], int(gato[2]), int(gato[2]),int(gato[3]), int(gato[4]), int(gato[5]), int(gato[6])))
            elif gato[1] == 'PAL':
                gatos.append(cl.Paladín(gato[0], int(gato[2]), int(gato[2]),int(gato[3]), int(gato[4]), int(gato[5]), int(gato[6])))
            elif gato[1] == 'MDB':
                gatos.append(cl.MagoDeBatalla(gato[0], int(gato[2]), int(gato[2]),int(gato[3]), int(gato[4]), int(gato[5]), int(gato[6])))
    return [gatos, seguir0]