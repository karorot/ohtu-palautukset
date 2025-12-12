import config
from peli_io import peli_io
from tuomari import tuomari
from kps import KPS

class PeliTehdas:
    def __init__(self):
        self._tuomari = tuomari
        self._peli_io = peli_io

    def luo_peli(self, valinta: str):
        if valinta.endswith(config.PVP):
            return KPS.pelaaja_vs_pelaaja(self._tuomari, self._peli_io)

        if valinta.endswith(config.AI):
            return KPS.pelaaja_vs_tekoaly(self._tuomari, self._peli_io)

        if valinta.endswith(config.PAREMPI_AI):
            return KPS.pelaaja_vs_parannettu_tekoaly(self._tuomari, self._peli_io, config.MUISTI)

        return None
