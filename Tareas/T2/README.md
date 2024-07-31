# Tarea 2: DCCombatientes 🐈⚔️


_Creo_ que logré implementar toda la tarea. Sin embargo, considero que por tiempo, no pude dejar el código lo más ordenado posible y los menus pueden verse un poco desordenados

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas 

#### Programación Orientada a Objetos: 12 pts (10%)
##### ✅ Definición de clases, herencia y *properties*
Se usan clases abstractas (combatientes), multiherencia (combatienetes evolucionados), properties (casi todos los atributos del ejército).

#### Preparación del programa: 10 pts (8%)
##### ✅ Inicio de la partida
Al iniciar, se lee archivo correspondiente a dado por terminal y se abre menú de inicio.

#### Entidades: 56 pts (47%)
##### ✅ Ejército
Ejército instanciado para jugador y para oponente (con métodos y atributos de enunciado).
##### ✅ Combatientes
Se crea la clase combatientes y se heredan de las formas que indica el enunciado.
##### ✅ Ítems
Compra de ítems para evoluscionar funciona correctamente.

#### Flujo del programa: 30 pts (25%)
##### ✅ Menú de Inicio
Funciona, puede recibir inputs erroneos y reportar.
##### ✅ Menú Tienda
Funciona, puede recibir inputs erroneos y reportar.
##### ✅ Selección de gato
Funciona, puede recibir inputs erroneos y reportar.
##### ✅ Fin del Juego
juego termina solo cuando jugador sale o cuando ya ha ganado.
##### ✅ Robustez
No entiendo a que se refiere D:.

#### Archivos: 12 pts (10%)
##### ✅ Archivos .txt
##### ✅ parametros.py
Se crea archivo con valores constantes que se importa en el código del flujo


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```Flujo.py```. En la terminal se debe escribir  ```python Flujo.py facil```, o cualquier dificultad que se quiera agregar. 


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```abc```: ```ABC``` y ```abstractmethod```
2. ```random```: ```random```  y ```choice```
3. ```copy```
4. ```sys.argv```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```Auxiliares```: Contiene a ```instanciar_oponente```, que instancia los gatos y los deja como una lista.
2. ```Graficas```: Contiene funciones para imprimir los menú.
3. ```Clases_cambio_atacar```: Contiene las clases ejércitos y combatientes (y sus hijos).

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. He asumido que los gatos comprados siempren parten con toda la vida completa.
2. He asumido que no existen empates al final de una ronda, porque el enunciado no dice nada al respecto.
3. He asumido que al comprar 2 gatos iguales, se creerán 2 instancias para cada uno. Así, uno puede comprar más de 6 gatos en un inicio.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).