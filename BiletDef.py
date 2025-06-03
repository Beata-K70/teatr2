import SalaDef
import ImprezaDef
import TeatrDB


class Bilet:
    def __init__(self):
        self.id = -1
        self.kategoria = ""
        self.rzad = ""
        self.miejsce = 0
        self.cena = 0
        self.impreza_id = 0
        self.klient_id = 0

    def __str__(self):
        return f'R{self.rzad}M{self.miejsce}:{self.kategoria}  impreza_id:{self.impreza_id} klient_id:{self.klient_id}'

    @staticmethod
    def daj_wypelniony(krzeslo, impreza):
        bilet = Bilet()
        bilet.kategoria = krzeslo.kategoria
        bilet.rzad = krzeslo.rzad
        bilet.miejsce = krzeslo.miejsce
        bilet.cena = impreza.daj_cene(krzeslo.kategoria)
        bilet.impreza_id = impreza.id
        bilet.klient_id = TeatrDB.PUSTY_KLIENT
        return bilet

    def laduj_z_tablicy(self, tab):
        self.id = tab[0]
        self.kategoria = tab[1]
        self.rzad = tab[2]
        self.miejsce = tab[3]
        self.cena = tab[4]
        self.impreza_id = tab[5]
        self.klient_id = tab[5]

    def daj_jako_tablica(self):
        return (self.kategoria,  # świadomie pomijam 'id'
                self.rzad,
                self.miejsce,
                self.cena,
                self.impreza_id,
                self.klient_id)
