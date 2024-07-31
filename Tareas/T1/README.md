# Tarea 1: DCCiudad 🚈🐈 .


Tanto la parte 1 como la 2 hacen lo pedido por el enunciado de la tarea:

- **Parte 1**: El archivo red.py contiene la clase RedMetro con sus respectivos métodos, que se discutirán más adelante.
- **Parte 2**: El archivo main.py contiene el código para el menú que se trabja en la terminal.

## Consideraciones generales

### Métodos implementados (Auxiliares):
La impletemntación de estos métodos son para asistir el método ```asegurar_ruta```. Algo importante de notar es que debido a una mala lectura del enunciado, el método ```asegurar_ruta``` computa todos las posibles sub-redes que cumplen la propiedad de distancia mínima. Arreglé esto retornando la primera red (si existe) que se encontró. Esto puede resultar problemático ya que el algoritmo tarda $\mathcal{O}(2^t)$ donde $t$ es la cantidad de túneles de la red original. De todas formas mi computador no tuvo problemas para los test públicos.

- **minima_distancia**: Dados los nombres de las estaciones de inicio y destino, calcula la menor cantidad de estaciones intermedias necesarias para ir de inicio o destino en una red que se entrega como argumento.
- **cambiar_por_binario**: Recibe un string de largo $t$ (número de túneles) que contiene solo ceros y unos y cambia la entrada número $i$ que es 1 (de la red original) por el número en la posición $i$ del string. Esto sirve para generar una sub-red.
- **numeros_binarios**: Entrega una lista con todos los strings de largo $t$ (número de túneles) compuestos por ceros y unos.
- **subgrafos**: Retorna lista de todas las sub-redes de la red original.

### Parte 2

Para la parte 2, el usuario deberá ingresar a la terminal de la carpeta T1. Ahí se deberá escribir ```python main.py *archivo* *estación*``` (por ejemplo ```python main.py test_1 Mirador``` ). Al menos en mi computador, escribir python3.11 lanzaba error, por lo que trabajé solo con el comando "python". Hecho esto, se desplegará el menú de acciones, cuyas instrucciones aparecerán en la terminal.
#### Menú: 13 pts (21,7%)
##### ✅ Consola
Funcionamiento de los métodos entregado en la tarea.
##### ✅ Menú de Acciones
Flujo entregado en el enunciado.
##### ✅ Modularización
Ningún archivo tiene más de 400 lineas.
###### ✅ PEP8


## Ejecución :computer:
La parte 1 se encuentra en su totalidad en el archivo  ```red.py```. Para la parte 2, se debe ingresar a la consola desde la carpeta ```T1``` y trabajar desde ahí. Este flujo se encuentra en el archivo ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```sys```: Usado en ```main.py``` para la lectura de datos desde la terminal.
2. ```copy```: Usado en varios módulos de ```red.py``` para copiar listas y listas de listas.
3. ```os```: Lo agregué en ```red.py```, pero no recuerdo la razón y me da miedo borrarlo XD.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```red.py```: Contiene la clase ```RedMetro``` pedida por el enunciado que se utiliza en la parte 2.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En la mayoría de los métodos y de funciones en la parte 2, los archivos y las estaciones que se escriben existen y son válidas para cierta red.

## Descuentos
Ojalá no tener :).