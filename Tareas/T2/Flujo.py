import Clases_cambio_atacar as cl 
from Graficas import menu_inicio, menu_tienda, selecciona_gato
from sys import argv
from Auxiliares import instanciar_oponente
from random import choice
import parametros as pm
import copy

#Lectura dificultad y datos
args = argv
dificultad = args[1]
seguir = True

if dificultad == 'facil':
    with open("data/facil.txt", "r") as file:
        contenido = file.read()
elif dificultad == 'intermedio':
     with open("data/intermedio.txt", "r") as file:
        contenido = file.read()
elif dificultad == 'dificil':
     with open("data/dificil.txt", "r") as file:
        contenido = file.read()
else:
     seguir = 'False'
     print('ERROR: Línea en terminal no válida')

with open("data/unidades.txt", "r") as file:
        unidades = file.read()

#Instanciar Gatos Oponentes de .txt
if seguir: 
    res = instanciar_oponente(contenido)
    seguir = (res[1] == 1)
    gatos_oponentes = res[0]

#Sacar gatos de unidades
if seguir: 
    res = instanciar_oponente(unidades)
    seguir = (res[1] == 1)
    unidades = res[0]

guerreros = []
magos = []
caballeros = []

for gato in unidades:
    clase = gato.__class__.__name__

    if clase == 'Guerrero':
        guerreros.append(gato)
    elif clase == 'Mago':
        magos.append(gato)
    elif clase == 'Caballero':
        caballeros.append(gato)

#Crear ejército
ej = cl.Ejercito()
ej_opuesto = cl.Ejercito()

ej.oro = pm.ORO_INICIAL
ej_opuesto.combatientes = [gatos_oponentes[0], gatos_oponentes[1], gatos_oponentes[2]]

#Rondas
ronda = 1
while seguir:
    menu_inicio(ej.oro, ronda)
    opcion = input()
    if opcion not in ['0', '1', '2', '3']:
        print()
        print('*****ERROR: OPCIÓN NO VÁLIDA*****')
        print('Volviendo al menú')
        print()
    elif opcion == '0':
        seguir = False
    elif opcion == '1':
        seguir_tienda = True

        #ENTRO A TIENDA
        while seguir_tienda:
            menu_tienda(ej.oro)
            opcion = input()

            if opcion not in ['0', '1', '2', '3', '4', '5', '6', '7']:
                    print()
                    print('*****ERROR: OPCIÓN NO VÁLIDA*****')
                    print('Volviendo al menú')
                    print()

            elif opcion == '0':
                 print('Saliendo de Tienda')
                 seguir_tienda = False

            elif opcion == '1':
                if ej.oro >= pm.PRECIO_MAG:
                    gato_comprado = choice(magos)
                    gato_copia = copy.deepcopy(gato_comprado)
                    ej.combatientes.append(gato_copia)
                    ej.oro -= pm.PRECIO_MAG
                    print(f'Se ha comprado a {gato_comprado.nombre}')
                    print(f'Tienes {ej.oro} de dinero disponible')
                else:
                    print('No tienes dinero suficiente :(')

            elif opcion == '2':
                if ej.oro >= pm.PRECIO_GUE:
                    gato_comprado = choice(guerreros)
                    gato_copia = copy.deepcopy(gato_comprado)
                    ej.combatientes.append(gato_copia)
                    ej.oro -= pm.PRECIO_GUE
                    print(f'Se ha comprado a {gato_comprado.nombre}')
                    print(f'Tienes {ej.oro} de dinero disponible')
                else:
                    print('No tienes dinero suficiente :(')

            elif opcion == '3':
                if ej.oro >= pm.PRECIO_CAB:
                    gato_comprado = choice(caballeros)
                    gato_copia = copy.deepcopy(gato_comprado)
                    ej.combatientes.append(gato_copia)
                    ej.oro -= pm.PRECIO_CAB
                    print(f'Se ha comprado a {gato_comprado.nombre}')
                    print(f'Tienes {ej.oro} de dinero disponible')
                else:
                    print('No tienes dinero suficiente :(')

            elif opcion == '4':
                if ej.oro >= pm.PRECIO_ARMADURA:
                    #MAGOS Y GURERREROS
                    gatos = ej.combatientes
                    me_sirven = []
                    for gato in gatos:
                        clase = gato.__class__.__name__
                        if clase == 'Mago' or clase == 'Guerrero':
                            me_sirven.append(gato)
                    if len(me_sirven) == 0:
                        print('No tienes gatos para aplicar este ítem :(')
                    else:
                        selecciona_gato(me_sirven)
                        seleccion = input()
                        opciones_posibles = [str(i) for i in range(1, len(me_sirven) + 1)]
                        if seleccion not in opciones_posibles:
                            print('*****ERROR: OPCIÓN NO VÁLIDA*****')
                        else: 
                            ej.oro -= pm.PRECIO_ARMADURA
                            gato_seleccionado = me_sirven[int(seleccion) - 1]
                            nuevo = gato_seleccionado.evolucionar('Armadura')
                            for num in range(len(ej.combatientes)):
                                if ej.combatientes[num] == gato_seleccionado:
                                    ej.combatientes[num] = nuevo
                            print(f'Gato {nuevo.nombre} ha evolucionado a {nuevo.__class__.__name__}!')
                else:
                    print('No tienes dinero suficiente :(')

            elif opcion == '5':
                if ej.oro >= pm.PRECIO_PERGAMINO:
                    #CABALLEROS Y GURERREROS
                    gatos = ej.combatientes
                    me_sirven = []
                    for gato in gatos:
                        clase = gato.__class__.__name__
                        if clase == 'Caballero' or clase == 'Guerrero':
                            me_sirven.append(gato)
                    if len(me_sirven) == 0:
                        print('No tienes gatos para aplicar este ítem :(')
                    else:
                        selecciona_gato(me_sirven)
                        seleccion = input()
                        opciones_posibles = [str(i) for i in range(1, len(me_sirven) + 1)]
                        if seleccion not in opciones_posibles:
                            print('*****ERROR: OPCIÓN NO VÁLIDA*****')
                        else: 
                            ej.oro -= pm.PRECIO_PERGAMINO
                            gato_seleccionado = me_sirven[int(seleccion) - 1]
                            nuevo = gato_seleccionado.evolucionar('Pergamino')
                            for num in range(len(ej.combatientes)):
                                if ej.combatientes[num] == gato_seleccionado:
                                    ej.combatientes[num] = nuevo
                            print(f'Gato {nuevo.nombre} ha evolucionado a {nuevo.__class__.__name__}!')
                else:
                    print('No tienes dinero suficiente :(')
                
            elif opcion == '6':
                if ej.oro >= pm.PRECIO_LANZA:
                    #CABALLEROS Y MAGOS
                    gatos = ej.combatientes
                    me_sirven = []
                    for gato in gatos:
                        clase = gato.__class__.__name__
                        if clase == 'Caballero' or clase == 'Mago':
                            me_sirven.append(gato)
                    if len(me_sirven) == 0:
                        print('No tienes gatos para aplicar este ítem :(')
                    else:
                        selecciona_gato(me_sirven)
                        seleccion = input()
                        opciones_posibles = [str(i) for i in range(1, len(me_sirven) + 1)]
                        if seleccion not in opciones_posibles:
                            print('*****ERROR: OPCIÓN NO VÁLIDA*****')
                        else: 
                            ej.oro -= pm.PRECIO_LANZA
                            gato_seleccionado = me_sirven[int(seleccion) - 1]
                            nuevo = gato_seleccionado.evolucionar('Lanza')
                            for num in range(len(ej.combatientes)):
                                if ej.combatientes[num] == gato_seleccionado:
                                    ej.combatientes[num] = nuevo
                            print(f'Gato {nuevo.nombre} ha evolucionado a {nuevo.__class__.__name__}!')
                else:
                    print('No tienes dinero suficiente :(')
            
            elif opcion == '7':
                if ej.oro >= pm.PRECIO_CURA:
                    print(f'Curando todos tus gatos en {pm.CURAR_VIDA}')
                    ej.oro -= pm.PRECIO_CURA
                    for gato in ej.combatientes:
                        gato.curarse(pm.CURAR_VIDA)
                else:
                    print('No tienes dinero suficiente :(')

        #SALGO DE TIENDA

    #Imprimir ejército.
    elif opcion == '2':
        print(ej)

    #Combatir
    elif opcion == '3':
        res = ej.combatir(ej_opuesto)
        if res == 1:
            print('Felicitaciones, has ganado!')
            print('Pasas a la siguiente ronda :D')
            ej.oro += pm.ORO_GANADO

            ej_opuesto.combatientes = [gatos_oponentes[3 * ronda - 3], gatos_oponentes[3 * ronda - 2], gatos_oponentes[3 * ronda - 1]]
            ronda += 1

        elif res == 0:
            print('Has empatado')
            #QUE HAGO ACÁ???????

        elif res == -1:
            print('GAME OVER')
            #Crear ejército
            ej = cl.Ejercito()
            ej_opuesto = cl.Ejercito()
            ej.dinero = pm.ORO_INICIAL
            ronda = 1
            seguir = True
            print('Parte de nuevo :)')
    
    if ronda == 4:
        seguir = False

print()
print('-' * 30)
print('Felicitaciones, Has ganado! Devoraste y no dejaste migajas.')
print('-' * 30)
print()