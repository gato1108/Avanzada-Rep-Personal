from utilidades import Animales, Candidatos, Distritos, Locales, Ponderador, Votos

def cargar_datos_lejos(tipo_generator: str, tamano: str):
    tipo_generator = tipo_generator[0].upper() + tipo_generator[1:]
    ruta = 'data/' + tamano + '/' + tipo_generator + '.csv'
    f = open(ruta, "r", encoding='latin-1')
    r = f.readlines()

    if tipo_generator == 'Animales':
        for linea in r:
            con = linea.strip('\n').split(',')
            if not con[0] == 'id':
                tup = Animales(int(con[0]), str(con[1]), str(con[2]), int(con[3]), 
                               float(con[4]), int(con[5]), str(con[6]))
                yield tup

    elif tipo_generator == 'Candidatos':
        for linea in r:
            con = linea.strip('\n').split(',')
            if not con[0] == 'id_candidato':
                tup = Candidatos(int(con[0]), str(con[1]), int(con[2]), str(con[3]))
                yield tup

    elif tipo_generator == 'Distritos':
        for linea in r:
            con = linea.strip('\n').split(',')
            if not con[0] == 'id_distrito':
                tup = Distritos(int(con[0]), str(con[1]), int(con[2]), 
                                str(con[3]), str(con[4]))
                yield tup

    elif tipo_generator == 'Locales':
        for linea in r:
            con = linea.strip('\n').split(',')
            a = linea.strip('\n').split('[')
            con = a[0].split(',')
            if not con[0] == 'id_local':
                l = a[1].strip(']').split(',')
                con[3] = []
                if not l[0] == '':
                    con[3] = [int(x) for x in l]
                tup = Locales(int(con[0]), str(con[1]), int(con[2]), con[3])
                yield tup

    elif tipo_generator == 'Ponderadores':
        for linea in r:
            con = linea.strip('\n').split(',')
            if not con[0] == 'especie':
                tup = Ponderador(str(con[0]), float(con[1]))
                yield tup

    elif tipo_generator == 'Votos':
        for linea in r:
            con = linea.strip('\n').split(',')
            if not con[0] == 'id_voto':
                tup = Votos(int(con[0]), int(con[1]), int(con[2]), int(con[3]))
                yield tup

    f.close()