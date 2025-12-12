import config

class peliIO:
    def lue_ekan_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    def lue_tokan_siirto(self):
        return input("Toisen pelaajan siirto: ")

    def tekoalyn_siirto(self, siirto):
        print(f"Tietokone valitsi: {siirto}")

    def validoi_siirto(self, siirto):
        return siirto in (config.KIVI, config.PAPERI, config.SAKSET)

    def lopeta_peli(self):
        print("Kiitos!")


peli_io = peliIO()
