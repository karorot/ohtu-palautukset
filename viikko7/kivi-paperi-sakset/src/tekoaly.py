import config

class Tekoaly:
    '''Yksinkertainen tekoäly'''
    def __init__(self):
        self._siirto = 0

    def anna_siirto(self):
        self._siirto = self._siirto + 1
        self._siirto = self._siirto % 3

        if self._siirto == 0:
            return config.KIVI
        elif self._siirto == 1:
            return config.PAPERI
        else:
            return config.SAKSET

    def aseta_siirto(self, siirto):
        # ei tehdä mitään
        pass
