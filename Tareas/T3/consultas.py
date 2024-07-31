from typing import Generator
from utilidades import Animales, Candidatos, Distritos, Locales, Ponderador, Votos
from functools import reduce
from itertools import product, tee, combinations
from collections import Counter, namedtuple
from carga_datos import cargar_datos_lejos

# ----------------------------------------------------------------------
# COMPLETAR
# ----------------------------------------------------------------------
#####RECORDAR 100 caracteressssssssssssssss y 400 lineaaaaas

# CARGA DE DATOS

def cargar_datos(tipo_generator: str, tamano: str):
    return cargar_datos_lejos(tipo_generator, tamano)

# 1 GENERADOR

def animales_segun_edad(generador_animales: Generator,
    comparador: str, edad: int) -> Generator:
    if comparador == '=':
        filtrado = filter(lambda x: x[5] == edad, generador_animales)
    elif comparador == '<':
        filtrado = filter(lambda x: x[5] < edad, generador_animales)
    elif comparador == '>':
        filtrado = filter(lambda x: x[5] > edad, generador_animales)
    mapeo = map(lambda x: x[1], filtrado)
    return mapeo


def animales_que_votaron_por(generador_votos: Generator,
    id_candidato: int) -> Generator:    
    filtrado = filter(lambda x: x[3] == id_candidato, generador_votos)
    mapeo = map(lambda x: x[1], filtrado)
    return  mapeo


def cantidad_votos_candidato(generador_votos: Generator,
    id_candidato: int) -> int:
    filtrado = filter(lambda x: x[3] == id_candidato, generador_votos)
    red = reduce(lambda x, y: x+1 , filtrado, 0)
    return int(red)


def ciudades_distritos(generador_distritos: Generator) -> Generator:
    mapeo = map(lambda x: x[3], generador_distritos)
    red = {x for x in mapeo}
    for elemento in red:
        yield elemento

def especies_postulantes(generador_candidatos: Generator,
    postulantes: int) ->Generator:
    mapeo = map(lambda x: x[3], generador_candidatos)
    contador = Counter()
    for especie in mapeo:
        contador[especie] += 1
    for especie in contador.keys():
        if contador[especie] >= postulantes:
            yield especie


def pares_candidatos(generador_candidatos: Generator) -> Generator:
    nombres = map(lambda x: x[1], generador_candidatos)
    prod = combinations(nombres, 2)
    for par in prod:
        yield (par[0], par[1])


def votos_alcalde_en_local(generador_votos: Generator, candidato: int,
    local: int) -> Generator:
    fil = filter(lambda x: (x[2] == local) and (x[3] == candidato), generador_votos)
    return fil


def locales_mas_votos_comuna (generador_locales: Generator,
    cantidad_minima_votantes: int, id_comuna: int) -> Generator:
    comuna = filter(lambda x: x[2] == id_comuna, generador_locales)
    votos = filter(lambda x: len(x[3]) >= cantidad_minima_votantes, comuna)
    for i in votos:
        yield i[0]


def votos_candidato_mas_votado(generador_votos: Generator) -> Generator:
    votos_resumen = {x[0]: x[3] for x in generador_votos}
    contador = Counter()
    for voto in votos_resumen.keys():
        contador[votos_resumen[voto]] += 1
    q_max = max(contador.values())
    res = [key for key in contador if contador[key] == q_max]
    id_max = max(res)
    for voto in votos_resumen.keys():
        quien_voto = votos_resumen[voto]
        if quien_voto == id_max:
            yield voto

        
def animales_segun_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator, comparador: str,
    edad: int) -> Generator:
    conversion = {especie[0]: especie[1] for especie in generador_ponderadores}
    if comparador == '=':
        for animal in generador_animales:
            especie = animal[2]
            conv = float(conversion[especie])
            edad_humana = animal[5] * conv
            if edad_humana == edad:
                yield animal[1]
    elif comparador == '>':
        for animal in generador_animales:
            especie = animal[2]
            conv = float(conversion[especie])
            edad_humana = animal[5] * conv
            if edad_humana > edad:
                yield animal[1]
    elif comparador == '<':
        for animal in generador_animales:
            especie = animal[2]
            conv = float(conversion[especie])
            edad_humana = animal[5] * conv
            if edad_humana < edad:
                yield animal[1]

# 2 GENERADORES

def animal_mas_viejo_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator) -> Generator:
    conversion = {especie[0]: especie[1] for especie in generador_ponderadores}
    it_anim = tee(generador_animales, 2) 
    edades = {animal[0]: (animal[5] * float(conversion[animal[2]])) for animal in it_anim[0]}
    nombres = {animal[0]: animal[1] for animal in it_anim[1]}
    max_val = max(edades.values())
    for animal in edades.keys():
        if edades[animal] == max_val:
            yield nombres[animal]


def votos_por_especie(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    id_votos = map(lambda x: x[3], generador_votos)
    contador =  Counter()
    for id in id_votos:
        contador[id] += 1
    especies = {id[0] : id[3] for id in generador_candidatos} 
    contador_2 = Counter()
    for id in especies.keys():
        contador_2[especies[id]] += contador[id]
    for especie in contador_2.keys():
        yield (especie, contador_2[especie])



def hallar_region(generador_distritos: Generator,
    generador_locales: Generator, id_animal: int) -> str:
    filtrado = filter(lambda x: id_animal in x[3], generador_locales)
    id_comuna = next(filtrado)[2]
    filtrado = filter(lambda x: x[2] == id_comuna, generador_distritos)
    return next(filtrado)[4]


def max_locales_distrito(generador_distritos: Generator,
    generador_locales: Generator) -> Generator:
    id_comunas = map(lambda x: x[2], generador_locales)
    contador = Counter()
    for id in id_comunas:
        contador[id] += 1
    comunas = {distrito[2]: distrito[1] for distrito in generador_distritos}
    contador_distritos = Counter()
    for comuna in comunas.keys():
        contador_distritos[comunas[comuna]] += contador[comuna]
    maximo = max(contador_distritos.values())
    for distrito in contador_distritos.keys():
        if contador_distritos[distrito] == maximo:
            yield distrito
    

def votaron_por_si_mismos(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    filtrado = filter(lambda x: x[1] == x[3], generador_votos)
    id_candidatos = map(lambda x: x[3], filtrado)
    id_candidatos_lista = [x for x in id_candidatos]
    for candidato in generador_candidatos:
        if candidato[0] in id_candidatos_lista:
            yield candidato[1]


def ganadores_por_distrito(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    contador = Counter()
    iterator1, iterator2 = tee(generador_candidatos, 2) 
    for voto in generador_votos:
        contador[voto[3]] += 1
    nombres = {candidato[0]: candidato[1] for candidato in iterator1}
    distritos = {candidato[0]: candidato[2] for candidato in iterator2}
    total_distritos = {distritos[dis] for dis in distritos.keys()}
    for dis in total_distritos:
        ids = [candidato for candidato in distritos.keys() if dis == distritos[candidato]]
        pares = combinations(ids, 2)
        for par in pares:
            prim = par[0]
            seg = par[1]
            if contador[prim] > contador[seg]:
                yield nombres[prim]
            elif contador[prim] < contador[seg]:
                yield nombres[seg]
            elif contador[prim] == contador[seg]:
                yield nombres[seg]
                yield nombres[prim]

# 3 o MAS GENERADORES

def mismo_mes_candidato(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator,
    id_candidato: str) -> Generator:
    votos_por_candidatos = filter(lambda x: x[3] == int(id_candidato), generador_votos)
    id_votantes = map(lambda x: x[1], votos_por_candidatos)
    fechas = {animal[0]: animal[6].split('/') for animal in generador_animales}
    id_candidatos = [candidato[0] for candidato in generador_candidatos]
    if id_candidato not in id_candidatos:
        return id_votantes
    fecha_candidato = fechas[id_candidato]
    for id in id_votantes:
        fecha = fechas[id]
        if fecha[0] ==  fecha_candidato[0] or fecha[1] ==  fecha_candidato[1]:
            yield id


def edad_promedio_humana_voto_comuna(generador_animales: Generator,
    generador_ponderadores: Generator, generador_votos: Generator,
    id_candidato: int, id_comuna:int ) -> float:
    animales_de_comuna = filter(lambda x: x[3] == int(id_comuna), generador_animales)
    votos = {voto[1]: voto[3] for voto in generador_votos}
    animales_votantes = filter(lambda x: votos[x[0]] == int(id_candidato), animales_de_comuna)
    conversion = {especie[0]: especie[1] for especie in generador_ponderadores}
    edades = [conversion[animal[2]] * animal[5] for animal in animales_votantes]
    if len(edades) == 0:
        return 0
    else:
        return(float(sum(edades) / len(edades)))


def votos_interespecie(generador_animales: Generator,
    generador_votos: Generator, generador_candidatos: Generator,
    misma_especie: bool = False,) -> Generator:
    especies_candidatos = {candidato[0]: candidato[3] for candidato in generador_candidatos}
    votos = {animal[1]: especies_candidatos[animal[3]] for animal in generador_votos}
    if misma_especie == True:
        for animal in generador_animales:
            id = animal[0]
            if id in votos.keys():
                especie_de_voto = votos[id]
                if especie_de_voto == animal[2]:
                    yield animal
    else:
        for animal in generador_animales:
            id = animal[0]
            if id in votos.keys():
                especie_de_voto = votos[id]
                if not especie_de_voto == animal[2]:
                    yield animal
    

def porcentaje_apoyo_especie(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator) -> Generator:
    especies = {animal[0]: animal[2] for animal in generador_animales}
    votos_por_id = {voto[1]: voto[3] for voto in generador_votos}
    total_especies = {esp: 0 for esp in especies.values()}
    #candidatos = {candidato[0]: candidato[3] for candidato in generador_candidatos}
    #especie = 'Gato'
    #x = [votos[3] for votos in generador_votos if especies[votos[1]] == especie]
    #votos_por_especie = {especie: [votos[3] for votos in generador_votos if
     #especies[votos[1]] == especie] for especie in total_especies}
   # votos_por_especie = {esp: 0 for esp in especies.values()}
    #for especie in total_especies.keys():
     #   votos_por_especie[especie] = [votos[3] for votos in 
     #generador_votos if especies[votos[1]] == especie] 
    votos_por_especie = {especie: [votos_por_id[votos] for votos in votos_por_id.keys() 
                                   if especies[votos] == especie] for especie in total_especies}

    for candidato in generador_candidatos:
        especie_candidato = candidato[3]
        if especie_candidato in votos_por_especie.keys():
            votos_especie = votos_por_especie[especie_candidato]
            a_favor = votos_especie.count(candidato[0])
            tot = len(votos_especie)
            if tot > 0:
                yield (candidato[0], round(a_favor * 100 / tot))
            else: 
                yield (candidato[0], 0)
        else:
            yield (candidato[0], 0)


def votos_validos(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores) -> int:
    conversion = {especie[0]: especie[1] for especie in generador_ponderadores}
    animal_edad = {animal[0]: (2024 - int(animal[6].split('/')[0])) * conversion[animal[2]] 
                   for animal in generador_animales}
    filtrado = filter(lambda x: animal_edad[x[1]] >= 18, generador_votos)
    lista = [id for id in filtrado]
    return len(lista)


def cantidad_votos_especie_entre_edades(generador_animales: Generator,
    generador_votos: Generator, generador_ponderador: Generator,
    especie: str, edad_minima: int, edad_maxima: int) -> str:
    conversion = {especie[0]: especie[1] for especie in generador_ponderador}
    animal_filtrado = filter(lambda x: x[2] == especie, generador_animales)
    votantes = {voto[0] for voto in generador_votos}
    votantes_especie =  filter(lambda x: x[0] in votantes, animal_filtrado)
    animal_edad = {animal[0]: animal[5] * conversion[animal[2]] for animal in votantes_especie}
    filtrado_1 = filter(lambda x: animal_edad[x] > edad_minima, animal_edad.keys())
    filtrado_2 = filter(lambda x: animal_edad[x] < edad_maxima, filtrado_1)
    lista = [id for id in filtrado_2]
    s_1 = f'Hubo {len(lista)} votos emitidos por animales entre'
    s_2 = f' {edad_minima} y {edad_maxima} años de la especie {especie}.'
    return s_1 + s_2


def distrito_mas_votos_especie_bisiesto(generador_animales: Generator,
    generador_votos: Generator, generador_distritos: Generator,
    especie: str) -> str:
    animales_especie = filter(lambda x: x[2] == especie, generador_animales)
    especie_biciesto = filter(lambda x: int(x[6].split('/')[0]) % 4 == 0, animales_especie)
    animales_votantes = [voto[1] for voto in generador_votos]
    votantes_biciestos = filter(lambda x:  x[0] in animales_votantes, especie_biciesto)
    comuna = [animal[3] for animal in votantes_biciestos]
    comuna_y_distrito = {com[2]: com[0] for com in generador_distritos}
    distritos = [comuna_y_distrito[com] for com in comuna]
    counter = Counter(distritos)
    min_max = min(comuna_y_distrito.values())
    if len(counter) > 0:
        max_dis = max(counter.values())
        maximos = [id for id in counter.keys() if counter[id] == max_dis]
        min_max = min(maximos)
    s_1 =  f'El distrito {min_max} fue el que tuvo más votos emitidos por '
    s_2 = f'animales de la especie {especie} nacidos en año bisiesto.'
    return s_1 + s_2


def votos_validos_local(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator,
    id_local: int) -> Generator:
    conversion = {especie[0]: especie[1] for especie in generador_ponderadores}
    animal_edad = {animal[0]: conversion[animal[2]] * animal[5] for animal in generador_animales}
    filtrado = filter(lambda x: animal_edad[x[1]] >= 18 and x[2] == id_local, generador_votos)
    for voto in filtrado:
        yield voto[0]
    

def votantes_validos_por_distritos(generador_animales: Generator,
    generador_distritos: Generator, generador_locales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator) -> Generator:
    iteradores = tee(generador_animales, 2) 
    it_votos = tee(generador_votos, 2) 
    conversion = {especie[0]: especie[1] for especie in generador_ponderadores}
    animal_edad = {animal[0]: conversion[animal[2]] * animal[5] for animal in iteradores[0]}
    votos_validos = filter(lambda x: animal_edad[x[1]] >= 18, it_votos[0])
    id_animal_local = {voto[1]: voto[2] for voto in it_votos[1]}
    locales = {loc[0]: loc[2] for loc in generador_locales}
    distritos = {dis[2]: dis[0] for dis in generador_distritos}
    local_y_distrito = {loc: distritos[locales[loc]] for loc in locales.keys()}
    contador_1 = Counter()
    contador_2 = Counter()
    for voto in votos_validos:
        contador_1[voto[2]] += 1
    for loc in locales.keys():
        contador_2[local_y_distrito[loc]] += contador_1[loc]
    maxi = max(contador_2.values())
    dis_maximos = [dis for dis in contador_2.keys() if contador_2[dis] == maxi]
    id_min = min(dis_maximos)
    for animal in iteradores[1]:
        if local_y_distrito[id_animal_local[animal[0]]] in distritos.keys():
            if local_y_distrito[id_animal_local[animal[0]]] == id_min:
                yield animal