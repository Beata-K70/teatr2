"""
--------------------------------------------------------------
Definicja klasy 'Impreza'

--------------------------------------------------------------
Projekt kursu PYTHON
(c) 2025, Beata Kania
--------------------------------------------------------------
"""
from datetime import datetime, date

DATE_FORMAT = "%d.%m.%Y"


class Impreza:
    def __init__(self):
        self.id = -1
        self._nazwa = ""
        self._data = date.today()
        self._sala = ""
        self._cena = [0, 0, 0, 0]

    def __str__(self):
        return f'Impreza:{self._nazwa} Data: {self._data} Sala:{self._sala} Cena: A={self.cena[0]} B={self.cena[1]} C={self.cena[2]} D={self.cena[3]}'

    def kopiuj_z(self, zrodlo):
        self._nazwa = zrodlo._nazwa
        self._data = zrodlo._data
        self._sala = zrodlo._sala
        self._cena = zrodlo._cena

    def laduj_z_tablicy(self, tab):
        self.id = tab[0]
        self._nazwa = tab[1]
        self._data = tab[2]
        self._sala = tab[3]
        self._cena[0] = tab[4]
        self._cena[1] = tab[5]
        self._cena[2] = tab[6]
        self._cena[3] = tab[7]

    def daj_jako_tablica(self):
        return (self.nazwa,
                self.data,
                self.sala,
                self.cena[0],
                self.cena[1],
                self.cena[2],
                self.cena[3])


    def daj_cene(self, kategoria):
        if kategoria == 'A':
            return self._cena[0]
        elif kategoria == 'B':
            return self._cena[1]
        elif kategoria == 'C':
            return self._cena[2]
        elif kategoria == 'D':
            return self._cena[3]
        else:
            raise Exception("Nieznana kategoria:", kategoria)

    @property
    def nazwa(self):
        return self._nazwa

    @nazwa.setter
    def nazwa(self, nazwa):
        if nazwa != "":
            self._nazwa = nazwa
        else:
            raise Exception("Nazwa nie może być puste")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data > date.today():
            self._data = data
        else:
            raise Exception("Niepoprawna data imprezy. Nie można ustawić daty do tyłu")

    def setDateAsStr(self, data_str):
        try:
            dt = datetime.strptime(data_str, DATE_FORMAT)
        except Exception as e:
            raise Exception(f'Niepoprawna data imprezy. Wprowadź w formacie dd.mm.rrrr [{e}]')
        data = dt;

    @property
    def sala(self):
        return self._sala

    @sala.setter
    def sala(self, sala):
        if sala != "":
            self._sala = sala
        else:
            raise Exception("Nazwa nie może być puste")

    @property
    def cena(self):
        return self._cena

    @cena.setter
    def cena(self, cena):
        ok = False
        if len(cena) == 4:
            ok = True
            for v in cena:
                ok &= isinstance(v, (float,int)) & (v >= 0.0)
        if not ok:
            raise Exception("Niepoprawny format pola 'cena'")
        self._cena = cena
