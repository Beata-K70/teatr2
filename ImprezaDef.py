"""
--------------------------------------------------------------
Definicja klasy 'Impreza'

--------------------------------------------------------------
Projekt kursu PYTHON
(c) 2025, Beata Kania
--------------------------------------------------------------
"""
from datetime import datetime, date


class Impreza:
    def __init__(self):
        self._nazwa = ""
        self._data = date.today()
        self._sala = ""

    def __str__(self):
        return f'Impreza:{self._nazwa} Data: {self._data} Sala:{self._sala}'

    def kopiuj_z(self, zrodlo):
        self._nazwa = zrodlo._nazwa
        self._data = zrodlo._data
        self._sala = zrodlo._sala

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
            dt = datetime.strptime(data_str, "%d.%m.%Y")
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
