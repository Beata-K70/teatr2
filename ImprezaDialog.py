from tkinter import *
from BaseEntry import *
from KlientDef import *


class ImprezaForm(BaseForm):
    NEW_KLIENT = 101
    UPDATE_KLIENT = 102

    def __init__(self, parent, event, klient=None, nowy=True):

        self.klient = klient
        self.event = event
        self._varSala = tk.StringVar()

        super().__init__(parent)
        self.title('Impreza')

        self._nowy = nowy

        if not nowy:
            self._set_impreza(klient)

    def _get_form_size(self):
        return [320, 200]  # width x height

    def _add_edit_items(self, frame):
        labels = ["Imię, nazwisko", "Miescowość", "ulica", "email", "telefon"]

        for x in Klient.klient_items:
            idx = Klient.klient_items.index(x)
            self._add_edit_item(frame, labels[idx], self._varTab[idx])
        self._add_combobox_item(frame,"Wybór sali", self._varSala)

    def _set_impreza(self, klient):
        for x in Klient.klient_items:
            v = klient.daj_element(x)
            idx = Klient.klient_items.index(x)
            self._varTab[idx].set(v)

    def _ok_btn_click(self):
        tmpKlient = Klient()
        dane_ok = True
        for x in Klient.klient_items:
            idx = Klient.klient_items.index(x)
            v = self._varTab[idx].get()
            if not tmpKlient.wstaw_element(x, v):
                dane_ok = False
                break
        if dane_ok:
            self.klient.kopiuj_z(tmpKlient)
            if self._nowy:
                self.event.set(self.NEW_KLIENT)
            else:
                self.event.set(self.UPDATE_KLIENT)
            self.destroy()
