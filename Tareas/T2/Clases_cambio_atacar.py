from abc import ABC, abstractmethod
from random import random
import parametros as pm


class Ejercito():

    def __init__(self):
        self.combatientes = []
        self.oro = 0

    def __str__(self):
        pass

    #Pelea de par de gatos
    def enfrentamiento(self, oponente):
        gato_mio = self.combatientes[0]
        gato_chico = oponente.combatientes[0]

        print(f'{gato_mio.nombre} está peleando con {gato_chico.nombre}!')
        
        while gato_mio.vida > 0 and gato_chico.vida > 0:
            ataque_1 = gato_mio.cambio_atacar(gato_chico)
            ataque_2 = gato_chico.cambio_atacar(gato_mio)
            gato_mio.atacar(gato_chico, ataque_1)
            gato_chico.atacar(gato_mio, ataque_2)

        if gato_mio.vida == 0:
            if gato_chico.vida == 0:
                oponente.combatientes.pop(0)
                self.combatientes.pop(0)
                print('Ambos han muerto juntos :O')
                return 0 #Empate
            else:
                print(f'{gato_chico.nombre} ha ganado! {gato_mio.nombre} ha muerto D:!')
                self.combatientes.pop(0)
                return -1 #Perdí
        elif gato_chico.vida == 0:
            oponente.combatientes.pop(0)
            print(f'{gato_mio.nombre} ha ganado! {gato_chico.nombre} ha muerto D:!')
            return 1 #Gané
        
    #Una ronda
    def combatir(self, oponente):
        while len(self.combatientes) > 0 and len(oponente.combatientes) > 0:
            print(f'Te quedan {len(self.combatientes)} gatitos para pelear!')
            print(f'Le quedan {len(oponente.combatientes)} a gato_chico para pelear!')
            resultado = self.enfrentamiento(oponente)

        if len(self.combatientes) == 0:
            if len(oponente.combatientes) == 0:
                return 0 #Empate
            else:
                return -1 #Perdí
        else:
            return 1 #Gané
        
    def __str__(self):
        print('-------Ejército Actual-------')
        print()
        for gato in self.combatientes:
            print(gato)
        print()
        print(f'Tienes {len(self.combatientes)} gatitos para pelear!')
        return ''

class Combatiente(ABC):
    #agilidad, poder, defensa cambian (settear dsp)
    def __init__(self, nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia):
        self.nombre = nombre
        self.vida_maxima = vida_maxima
        self.__vida = vida
        self.__poder = poder
        self.__defensa = defensa
        self.__agilidad = agilidad
        self.__resistencia = resistencia

    @property
    def poder(self):
        return self.__poder

    @poder.setter
    def poder(self, valor):
        if valor < 0:
            self.__poder = 0
        else:
            self.__poder = valor

    @property
    def defensa(self):
        return self.__defensa

    @defensa.setter
    def defensa(self, valor):
        if valor < 0:
            self.__defensa = 0
        else:
            self.__defensa = valor

    @property
    def agilidad(self):
        return self.__agilidad

    @agilidad.setter
    def agilidad(self, valor):
        if valor < 0:
            self.__agilidad = 0
        else:
            self.__agilidad = valor

    @property
    def resistencia(self):
        return self.__resistencia

    @resistencia.setter
    def resistencia(self, valor):
        if valor < 0:
            self.__resistencia = 0
        else:
            self.__resistencia = valor

    @property
    def ataque(self):
        return round(2 * self.vida * (self.poder + self.agilidad + self.resistencia) / self.vida_maxima)
    
    @abstractmethod
    def __str__(self):
        pass

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, valor):
        if valor < 0:
            self.__vida = 0
        elif valor < self.vida_maxima:
            self.__vida = valor
        else:
            self.__vida = self.vida_maxima

    @abstractmethod
    def atacar(self):
        pass

    @abstractmethod
    def evolucionar(self):
        pass

    def curarse(self, plus):
        self.vida += plus

class Guerrero(Combatiente):

    def __init__(self, nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia):
        super().__init__(nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia)

    def __str__(self):
        return f'Holi <3 Soy {self.nombre}, un gato guerrero con {self.vida} / {self.vida_maxima} de vida, ataque de {self.ataque} y defensa de {self.defensa}.'
    
    #Indica ataque que se tiene q dar
    def cambio_atacar(self, oponente):
        return [max(1, round(self.ataque - oponente.defensa)), 
                round((pm.CANSANCIO / 100) * self.agilidad),
                0]
    
    def atacar(self, oponente, cambio):

        oponente.vida -= cambio[0]
        self.agilidad -= cambio[1]
        self.resistencia -= cambio[2]


    def evolucionar(self, item):
        if item == 'Pergamino':
            gato_nuevo = MagoDeBatalla(self.nombre, self.vida_maxima, self.vida, self.poder, self.defensa, self.agilidad, self.resistencia)
            return  gato_nuevo
        elif item == 'Armadura':
            gato_nuevo = Paladín(self.nombre, self.vida_maxima, self.vida, self.poder, self.defensa, self.agilidad, self.resistencia)
            return  gato_nuevo
        else:
            return False

class Caballero(Combatiente):

    def __init__(self, nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia):
        super().__init__(nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia)

    def __str__(self):
        return f'Holi <3 Soy {self.nombre}, un gato caballero con {self.vida} / {self.vida_maxima} de vida, ataque de {self.ataque} y defensa de {self.defensa}.'
    
    def cambio_atacar(self, oponente):
        activa_poder = (pm.PROB_CAB >= random() * 100)
        if activa_poder:
            oponente.poder -= pm.RED_CAB * oponente.poder / 100
            atack = max(1, round(self.ataque * pm.ATQ_CAB / 100 - oponente.defensa))
        else:
            atack = max(1, round(self.ataque - oponente.defensa))
        return [atack, 
                0, 
                round((pm.CANSANCIO / 100) * self.resistencia)]
        
    def atacar(self, oponente, cambio):
        
        oponente.vida -= cambio[0]
        self.agilidad -= cambio[1]
        self.resistencia -= cambio[2]

    def evolucionar(self, item):
        if item == 'Pergamino':
            gato_nuevo = CaballeroArcano(self.nombre, self.vida_maxima, self.vida, self.poder, self.defensa, self.agilidad, self.resistencia)
            return  gato_nuevo
        elif item == 'Lanza':
            gato_nuevo = Paladín(self.nombre, self.vida_maxima, self.vida, self.poder, self.defensa, self.agilidad, self.resistencia)
            return  gato_nuevo
        else:
            return False

class Mago(Combatiente):

    def __init__(self, nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia):
        super().__init__(nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia)

    def __str__(self):
        return f'Holi <3 Soy {self.nombre}, un gato mago con {self.vida} / {self.vida_maxima} de vida, ataque de {self.ataque} y defensa de {self.defensa}.'
    
    def cambio_atacar(self, oponente):
        activa_poder = (pm.PROB_CAB >= random() * 100)
        if activa_poder:
            oponente.poder -= pm.RED_CAB * oponente.poder / 100
            atack = max(1, round(self.ataque * pm.ATQ_MAG / 100 - oponente.defensa * (100 - pm.RED_MAG) / 100))
        else:
            atack = max(1, round(self.ataque - oponente.defensa))
        return [atack, round((pm.CANSANCIO / 100) * self.agilidad),round( (pm.CANSANCIO / 100) * self.resistencia)]
    
    def atacar(self, oponente, cambio):
        
        oponente.vida -= cambio[0]
        self.agilidad -= cambio[1]
        self.resistencia -= cambio[2]

    def evolucionar(self, item):
        if item == 'Armadura':
            gato_nuevo = CaballeroArcano(self.nombre, self.vida_maxima, self.vida, self.poder, self.defensa, self.agilidad, self.resistencia)
            return  gato_nuevo
        elif item == 'Lanza':
            gato_nuevo = MagoDeBatalla(self.nombre, self.vida_maxima, self.vida, self.poder, self.defensa, self.agilidad, self.resistencia)
            return  gato_nuevo
        else:
            return False

class Paladín(Guerrero, Caballero):
    
    def __init__(self, nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia):
        super().__init__(nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia)

    def __str__(self):
        return f'Holi <3 Soy {self.nombre}, un gato paladín con {self.vida} / {self.vida_maxima} de vida, ataque de {self.ataque} y defensa de {self.defensa}.'
    
    def cambio_atacar(self, oponente):
        if random() * 100 < pm.PROB_PAL: #activa poder
            ataque = Caballero.cambio_atacar(self, oponente)
            activa = True
        else: #No activa poder
            ataque = Guerrero.cambio_atacar(self, oponente)
            activa = False
        return [ataque, activa]
    
    def atacar(self, oponente, cambio):  
        if cambio[1]:
            Caballero.atacar(self, oponente, cambio[0])
        else:
            Guerrero.atacar(self, oponente, cambio[0])
        self.resistencia += round(self.resistencia * pm.AUM_PAL / 100)

class MagoDeBatalla(Guerrero, Mago):
    
    def __init__(self, nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia):
        super().__init__(nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia)

    def __str__(self):
        return f'Holi <3 Soy {self.nombre}, un gato mago de batalla con {self.vida} / {self.vida_maxima} de vida, ataque de {self.ataque} y defensa de {self.defensa}.'

    def cambio_atacar(self, oponente):
        if random() * 100 < pm.PROB_MDB: #activa poder
            ataque = Mago.cambio_atacar(self, oponente)
            activa = True
        else: #No activa poder
            ataque = Guerrero.cambio_atacar(self, oponente)
            activa = False
        return [ataque, activa]
    
    def atacar(self, oponente, cambio):  
        if cambio[1]:
            Mago.atacar(self, oponente, cambio[0])
        else:
            Guerrero.atacar(self, oponente, cambio[0])

        self.defensa += round(self.defensa * pm.DEF_MDB / 100)
        self.agilidad -= round(self.agilidad * pm.CANSANCIO / 100)

class CaballeroArcano(Mago, Caballero):
    
    def __init__(self, nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia):
        super().__init__(nombre, vida_maxima, vida, poder, defensa, agilidad, resistencia)

    def __str__(self):
        return f'Holi <3 Soy {self.nombre}, un gato caballero arcano con {self.vida} / {self.vida_maxima} de vida, ataque de {self.ataque} y defensa de {self.defensa}.'

    def cambio_atacar(self, oponente):
        if random() * 100 < pm.PROB_CAR: #activa poder
            ataque = Caballero.cambio_atacar(self, oponente)
            activa = True
        else: #No activa poder
            ataque = Mago.cambio_atacar(self, oponente)
            activa = False
        return [ataque, activa]
    
    def atacar(self, oponente, cambio):  
        if cambio[1]:
            Caballero.atacar(self, oponente, cambio[0])
        else:
            Mago.atacar(self, oponente, cambio[0])

        self.poder += round(self.poder * pm.AUM_CAR / 100)
        self.agilidad += round(self.agilidad * pm.AUM_CAR / 100)
        self.resistencia -= round(self.resistencia * pm.CANSANCIO / 100)
