from abc import abstractmethod
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu


class KPS:
    def __init__(self, tuomari, io, tekoaly=None):
        self._tekoaly = tekoaly
        self._io = io
        self._tuomari = tuomari

    @staticmethod
    def pelaaja_vs_pelaaja(tuomari, io):
        return KPSPvP(tuomari, io)

    @staticmethod
    def pelaaja_vs_tekoaly(tuomari, io):
        tekoaly = Tekoaly()
        return KPSTekoaly(tuomari, io, tekoaly)

    @staticmethod
    def pelaaja_vs_parannettu_tekoaly(tuomari, io, muisti):
        tekoaly = TekoalyParannettu(muisti)
        return KPSTekoaly(tuomari, io, tekoaly)

    def pelaa(self):
        ekan_siirto = self._io.lue_ekan_siirto()
        tokan_siirto = self.tokan_siirto()

        while (
            self._io.validoi_siirto(ekan_siirto)
            and self._io.validoi_siirto(tokan_siirto)
        ):
            if self._tekoaly:
                self._io.tekoalyn_siirto(tokan_siirto)

            self._tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(self._tuomari)

            ekan_siirto = self._io.lue_ekan_siirto()
            tokan_siirto = self.tokan_siirto()

        self._io.lopeta_peli()

    @abstractmethod
    def tokan_siirto(self):
        pass


class KPSPvP(KPS):
    def __init__(self, tuomari, io):
        super().__init__(tuomari, io)

    def tokan_siirto(self):
        return self._io.lue_tokan_siirto()


class KPSTekoaly(KPS):
    def __init__(self, tuomari, io, tekoaly):
        super().__init__(tuomari, io, tekoaly)

    def tokan_siirto(self):
        return self._tekoaly.anna_siirto()
