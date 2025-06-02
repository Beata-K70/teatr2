"""
--------------------------------------------------------------
Definicja klasy 'Klient'

--------------------------------------------------------------
Projekt kursu PYTHON
(c) 2025, Beata Kania
--------------------------------------------------------------
"""

class Klient:
    def __init__(self):
        self.imie_nazwisko = ""
        self.miejscowosc = ""
        self.adres = ""
        self.email = ""
        self.telefon = ""

    def __str__(self):
        return f'Klient:{self.imie_nazwisko}, Adres:{self.miejscowosc}, ul.{self.adres}, email:{self.email}, telefon:{self.telefon}'

    def kopiuj_z(self, zrodlo):
        self.imie_nazwisko = zrodlo.imie_nazwisko
        self.miejscowosc = zrodlo.miejscowosc
        self.adres = zrodlo.adres
        self.email = zrodlo.email
        self.telefon = zrodlo.telefon





