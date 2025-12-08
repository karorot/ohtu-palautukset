class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo
        self._edelliset_arvot = [arvo]

    def miinus(self, operandi):
        self._arvo = self._arvo - operandi

    def plus(self, operandi):
        self._arvo = self._arvo + operandi

    def nollaa(self):
        self._arvo = 0
        self._edelliset_arvot = [0]

    def aseta_arvo(self, arvo):
        self._arvo = arvo

    def arvo(self):
        return self._arvo

    def tallenna_arvo(self):
        self._edelliset_arvot.append(self._arvo)

    def poista_viimeisin_arvo(self):
        if len(self._edelliset_arvot) > 1:
            self._edelliset_arvot.pop()
            return self._edelliset_arvot[-1]
