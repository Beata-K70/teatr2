"""
--------------------------------------------------------------
Definicja klasy 'Sala'

--------------------------------------------------------------
Projekt kursu PYTHON
(c) 2025, Beata Kania
--------------------------------------------------------------
"""

"""
definicja krzeseł
A - krzesło kategori A
B - krzesło kategori B
C - krzesło kategori C
D - krzesło kategori D

"""

# definicja dostepnych sal
sala_glowna = {"nazwa": "Główna",
               "krzesla": ["AAAAAAAA",
                           "AAAAAAAA",
                           "BBAAAABB",
                           "CCCBBCC",
                           "DDDCCAADDDD"]}

sala_mala = {"nazwa": "Mała",
             "krzesla": ["AAAA",
                         "BBBBBB",
                         "CCCCCCC",
                         "DDDDDDDD"]}

sala_elita = {"nazwa": "Elita",
              "krzesla": ["AAAA",
                          "AAAA",
                          "AAAA",
                          "AAAA"]}

lista_sal = [sala_glowna, sala_mala, sala_elita]


class Krzeslo:
    def __init__(self, kategoria, rzad, miejsce):
        self.kategoria = kategoria
        self.rzad = rzad
        self.miejsce = miejsce

    def __str__(self):
        return f'R{self.rzad}M{self.miejsce}:{self.kategoria}'


class Sala:
    def __init__(self, nazwa):
        fnd = False
        self._krzesla = []
        for x in lista_sal:
            if nazwa == x["nazwa"]:
                fnd = True
                self._krzesla = x["krzesla"]
        if not fnd:
            raise Exception("Niepoprawna nazwa sali")
        self._nazwa = nazwa

    def get_ilosc_krzesel(self):
        liczniki = [0, 0, 0, 0]
        for rzad in self._krzesla:
            for ch in rzad:
                if ch == 'A':
                    liczniki[0] += 1
                if ch == 'B':
                    liczniki[1] += 1
                if ch == 'C':
                    liczniki[2] += 1
                if ch == 'D':
                    liczniki[3] += 1
        wynik = []
        for x in range(4):
            ch = chr(ord('A') + x)
            wynik.append([ch, liczniki[x]])
        return wynik

    def buduj_lista_krzesel(self):
        lista = []
        nr_rzedu = 0
        for rzad_krzesel in self._krzesla:
            nr_rzedu += 1
            nr_miejsca = 0
            for ch in rzad_krzesel:
                nr_miejsca += 1
                krzeslo = Krzeslo(ch, nr_rzedu, nr_miejsca)
                lista.append(krzeslo)
        return lista

    def getj_suma_krzesel(self):
        lista = self.get_ilosc_krzesel()
        suma = 0
        for x in lista:
            suma += x[1]
        return suma


def daj_liste_sal():
    lista = []
    for x in lista_sal:
        lista.append(x["nazwa"])
    return lista


# ---Test----------------------------------
if __name__ == "__main__":
    print("\n\n------Sala-------")
    print(daj_liste_sal())
    sala = Sala("Główna")
    spis = sala.get_ilosc_krzesel()
    suma = 0
    for x in spis:
        print(x)
    print("Suma:", sala.getj_suma_krzesel())
    list_krzesel = sala.buduj_lista_krzesel()

    for x in list_krzesel:
        print(x)
