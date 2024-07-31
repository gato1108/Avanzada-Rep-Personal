import sys
import red
import dcciudad

#Lectura datos terminal
args = sys.argv

#Leer archivo (si es que existe)
red_test = red.RedMetro([],[])
nombre_archivo = args[1] + '.txt'
lectura = red_test.cambiar_planos(nombre_archivo)

print()
print('-------------------------------------Lectura de Datos-------------------------------------')
print()

if not lectura:
    print(f'El archivo {nombre_archivo} no se ha encontrado :(.')
else:
    print(f'Se ha leído con extito el archivo {nombre_archivo}!')
    estacion = args[2]
    if estacion in red_test.estaciones:
        print('Estación válida para la red :)')
    else: 
        print('No se ha encontrado la estación en la red :(')

#Menu de acciones

if lectura and estacion in red_test.estaciones:
    seguir = True
    while seguir:
        print()
        print('-------------------------------------Menú de Acciones-------------------------------------')
        print()
        print(f'Se está consultando por la estacion: {estacion} en la red {nombre_archivo}.')
        print()
        print('Seleccione una de las siguiente opciones (escribir 1, 2, 3 o 4):')
        print()
        print('1. Mostrar Red')
        print('2. Encontrar ciclo más corto')
        print('3. Asegurar Ruta')
        print('4. Salir del Programa')
        print()
        respuesta = int(input('Tu opción: '))
        print()
        if respuesta == 4:
            seguir = False
            print('Chau! Recuerda tomar agua.')
        elif respuesta == 1:
            dcciudad.imprimir_red(red_test.red, red_test.estaciones)
        elif respuesta == 2:
            ciclo = red_test.ciclo_mas_corto(estacion)
            if not ciclo == -1:
                print(f'El ciclo más corto que pasa por {estacion} pasa por {ciclo} estaciones intermedias.')
            else:
                print(f'No hay ciclo que pase por {estacion}.')
        elif respuesta == 3:
            inicio = input('Ingresar estación de inicio: ')
            destino = input('Ingresar estación de destino: ')
            p_intermedias = input('Ingresar número de estaciones intermedias: ')
            asegurar = red_test.asegurar_ruta(inicio, destino, p_intermedias)
            print('Se han encontrado las siguientes redes:')
            for red in asegurar:
                print('------------------------------------------')
                for fila in red:
                    print(fila)
