class Summa():
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote

    def suorita(self):
        arvo = self._lue_syote()
        self._sovelluslogiikka.plus(arvo)
        self._sovelluslogiikka.tallenna_arvo()

    def kumoa(self):
        edellinen_arvo = self._sovelluslogiikka.poista_viimeisin_arvo()
        self._sovelluslogiikka.aseta_arvo(edellinen_arvo)

class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote

    def suorita(self):
        arvo = self._lue_syote()
        self._sovelluslogiikka.miinus(arvo)
        self._sovelluslogiikka.tallenna_arvo()

    def kumoa(self):
        edellinen_arvo = self._sovelluslogiikka.poista_viimeisin_arvo()
        self._sovelluslogiikka.aseta_arvo(edellinen_arvo)

class Nollaus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote

    def suorita(self):
        self._sovelluslogiikka.nollaa()

    def kumoa(self):
        edellinen_arvo = self._sovelluslogiikka.poista_viimeisin_arvo()
        self._sovelluslogiikka.aseta_arvo(edellinen_arvo)
