import config
from pelitehdas import PeliTehdas

def main():
    pelitehdas = PeliTehdas()
    pelimoodit = [config.PVP, config.AI, config.PAREMPI_AI]

    while True:
        print("Valitse pelataanko"
              f"\n ({config.PVP}) Ihmistä vastaan"
              f"\n ({config.AI}) Tekoälyä vastaan"
              f"\n ({config.PAREMPI_AI}) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()
        if vastaus not in pelimoodit:
            break

        peli = pelitehdas.luo_peli(vastaus)

        print(
                "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin "
                f"{config.KIVI}, {config.PAPERI} tai {config.SAKSET}."
            )

        peli.pelaa()


if __name__ == "__main__":
    main()
