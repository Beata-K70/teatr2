from tkinter import *

import SalaDef
from BaseDialog import *
import ImprezaDef
import SalaDef
from datetime import datetime, date

from tkinter import messagebox


class ImprezaForm(BaseForm):
    NEW_IMPREZA = 111
    UPDATE_IMPREZA = 112

    def __init__(self, parent, event, impreza, nowy=True):

        self.impreza = impreza
        self.event = event
        self._nowy = nowy

        self._varNazwa = tk.StringVar()
        self._varData = tk.StringVar()
        self._varSala = tk.StringVar()
        self._varCenaA = tk.StringVar()
        self._varCenaB = tk.StringVar()
        self._varCenaC = tk.StringVar()
        self._varCenaD = tk.StringVar()


        super().__init__(parent)
        self.title('Impreza')

        if not nowy:
            self._set_impreza(impreza)

    def _get_form_size(self):
        return [320, 200]  # width x height

    def _add_edit_items(self, frame):

        nazwa_entry = self._add_edit_item(frame, "Nazwa", self._varNazwa)
        lista_sal = SalaDef.get_liste_sal()
        sala_entry = self._add_combobox_item(frame, "Sala", lista_sal, self._varSala)
        if not self._nowy:
            nazwa_entry.config(state="disabled")
            sala_entry.config(state="disabled")

        self._add_edit_item(frame, "Data", self._varData)
        self._add_edit_item(frame, "Cena kategorii A", self._varCenaA)
        self._add_edit_item(frame, "Cena kategorii B", self._varCenaB)
        self._add_edit_item(frame, "Cena kategorii C", self._varCenaC)
        self._add_edit_item(frame, "Cena kategorii D", self._varCenaD)

    def _clear_btn_click(self):
        self._varNazwa.set("")
        self._varData.set("")
        self._varSala.set("")
        self._varCenaA.set("")
        self._varCenaB.set("")
        self._varCenaC.set("")
        self._varCenaD.set("")

    def _set_impreza(self, impreza):
        self._varNazwa.set(impreza.nazwa)
        self._varData.set(impreza.data.strftime(ImprezaDef.DATE_FORMAT))
        self._varSala.set(impreza._sala)
        self._varCenaA.set(impreza.cena[0])
        self._varCenaB.set(impreza.cena[1])
        self._varCenaC.set(impreza.cena[2])
        self._varCenaD.set(impreza.cena[3])

    def _ok_btn_click(self):
        tmpImpreza = ImprezaDef.Impreza()
        try:
            tmpImpreza.nazwa = self._varNazwa.get()
            tmpImpreza.sala = self._varSala.get()
            tmpImpreza.setDateAsStr( self._varData.get())
            cena = [0.0,0.0,0.0,0.0]
            cena[0] = float(self._varCenaA.get())
            cena[1] = float(self._varCenaB.get())
            cena[2] = float(self._varCenaC.get())
            cena[3] = float(self._varCenaD.get())
            tmpImpreza.cena = cena

            self.impreza.kopiuj_z(tmpImpreza)
            if self._nowy:
                self.event.set(self.NEW_IMPREZA)
            else:
                self.event.set(self.UPDATE_IMPREZA)
            self.destroy()
        except Exception as e:
            messagebox.showerror(title="Błąd danych", message=e)

