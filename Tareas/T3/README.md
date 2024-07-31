# Tarea 3


### Cosas implementadas y no implementadas 

He rellenado las funciones dadas en el enunciado. Todas entregan "ok" con los tests case. 
En general, todas demoran menos de 5/6 segundos. Una consulta pasa los tests case en 9 segundos y otra la pasa en alrededor de 80 segundos. 
Hice mi mejor esfuerzo para optimizar esta última pero no logré hacerlo :(


## Ejecución 

Todas las funciones de consultas se encuentran en ```consultas.py```, sin embargo, para cumplir la restricción de 400 lineas, he creado el archivo ```carga_datos.py``` que contiene la verdadera función de este mismo nombre que debería estar en ```consultas.py```. El resto de los archivos son los entregados en el enunciado.


## Librerías 
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```typing```: ```Generator``` venía en el enunciado
2. ```functools```: ```reduce``` función que si no me equivoco, solo la importé al principio y no usé nunca.
3. ```itertools```: ```product``` Función que no recuerdo haber usado y solo importé por las moscas.
4. ```itertools```: ```tee``` Función para "copiar" generadores
5. ```itertools```: ```combinations``` La usé para sacara las combinaciones (candidato, candidato)
6. ```collections```: ```Counter``` Contador para contar votos (usualmente)
7. ```collections```: ```namedtuple``` Usado para función cargar datos


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```carga_datos```: Contiene a ```cargar_datos_lejos``` que es básicamente la función cargar_datos, pero la saqué para cumplir las 400 lineas.



-------

Por temas de espacio, no pude comentar que hacia cada parte de mi código (lo siento), por lo que intenté llamar las variables con nombres sugerentes de lo que querían hacer. 

## Descuentos
Probablemente tenga descuentos por el tiempo que tardan las funciones :(