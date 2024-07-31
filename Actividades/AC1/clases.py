from abc import ABC, abstractmethod
import random


class Vehiculo(ABC):
    identificador = 0
    def __init__(self, rendimiento, marca, energia = 120, *args, **kwargs):
        super().__init__(**kwargs)
        self.rendimiento = int(rendimiento)
        self.marca = str(marca)
        if energia < 0:
            self._energia = 0
        else:
            self._energia = energia
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador += 1
    
    @property
    def energia(self):
        return self._energia
    
    @energia.setter
    def energia(self, x):
        if x < 0:
            self._energia = 0
        else:
            self._energia = x
    
    @property
    def autonomia(self):
        return self.energia * self.rendimiento
    
    @abstractmethod
    def recorrer(self, kilometros):
        pass
    
    
class AutoBencina(Vehiculo):
    def __init__(self, bencina_favorita, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bencina_favorita = bencina_favorita

    def recorrer(self, kilometros):
        super().recorrer(kilometros)
        numero = min(self.autonomia, kilometros)
        L =  numero / self.rendimiento
        self.energia -= L
        return f"Anduve por {numero}Km y gaste {int(L)}L de bencina"


class AutoElectrico(Vehiculo):
    def __init__(self, vida_util_bateria, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vida_util_bateria = vida_util_bateria

    @property
    def vida_util_bateria(self):
        return self._vida_util_bateria
    
    def recorrer(self, kilometros):
        super().recorrer(kilometros)
        numero = min(self.autonomia, kilometros)
        L = numero / self.rendimiento
        self.energia -= L
        return f"Anduve por {numero}Km y gaste {int(L)}W de energia electrica"


class Camioneta(AutoBencina):
    def __init__(self, capacidad_maleta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._capacidad_maleta = capacidad_maleta
    
    @property
    def capacidad_maleta(self):
        return self._capacidad_maleta

class Telsa(AutoElectrico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros):
        res = super().recorrer(kilometros)
        return res+' de forma inteligente'


class FaitHibrido(AutoBencina, AutoElectrico):
    def __init__(self, vida_util_bateria = 5, *args, **kwargs):
        super().__init__(vida_util_bateria = 5, *args, **kwargs)
    
    def recorrer(self, kilometros):
        ab = AutoBencina.recorrer(self, kilometros/2)
        ae = AutoElectrico.recorrer(self, kilometros/2)
        return ab + ' ' + ae