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
        self.id = -1  # index z bazy danych
        self._imie = ""
        self._nazwisko = ""
        self.miejscowosc = ""
        self.adres = ""
        self._email = ""
        self.telefon = ""

    def __str__(self):
        return f'Klient:{self.imie} {self.nazwisko}, Adres:{self.miejscowosc}, ul.{self.adres}, email:{self.email}, telefon:{self.telefon}'

    def kopiuj_z(self, zrodlo):
        self.id = zrodlo.id
        self._imie = zrodlo._imie
        self._nazwisko = zrodlo._nazwisko
        self.miejscowosc = zrodlo.miejscowosc
        self.adres = zrodlo.adres
        self._email = zrodlo._email
        self.telefon = zrodlo.telefon

    def laduj_z_tablicy(self,tab):
        self.id = tab[0]
        self._imie = tab[1]
        self._nazwisko = tab[2]
        self.miejscowosc = tab[3]
        self.adres = tab[4]
        self._email = tab[5]
        self.telefon = tab[6]

    @property
    def imie(self):
        return self._imie

    @imie.setter
    def imie(self, imie):
        if imie != "":
            self._imie = imie
        else:
            raise Exception("Imie nie może być puste")

    @property
    def nazwisko(self):
        return self._nazwisko

    @nazwisko.setter
    def nazwisko(self, nazwisko):
        if nazwisko != "":
            self._nazwisko = nazwisko
        else:
            raise Exception("Nazwisko nie może być puste")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email != "":
            if "@" in email:
                self._email = email
            else:
                raise Exception("Niepoprawny email")
        else:
            raise Exception("Email nie może być pusty")
