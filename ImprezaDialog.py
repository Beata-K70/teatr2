from tkinter import *
from BaseDialog import *
from ImprezaDef import *
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

        super().__init__(parent)
        self.title('Impreza')

        if not nowy:
            self._set_impreza(impreza)

    def _get_form_size(self):
        return [320, 200]  # width x height

    def _add_edit_items(self, frame):

        nazaEntry = self._add_edit_item(frame, "Nazwa", self._varNazwa)
        if not self._nowy:
            nazaEntry.config(state="disabled")
        self._add_combobox_item(frame, "Sala", self._varSala)
        self._add_edit_item(frame, "Data", self._varData)

    def _clear_btn_click(self):
        self._varNazwa.set("")
        self._varData.set("")
        self._varSala.set("")

    def _set_impreza(self, impreza):
        self._varNazwa.set(impreza.nazwa)
        self._varData.set(impreza.data)
        self._varSala.set(impreza.sala)

    def _ok_btn_click(self):
        tmpImpreza = Impreza()
        try:
            tmpImpreza.nazwa = self._varNazwa.get()
            tmpImpreza.sala = self._varSala.get()
            tmpImpreza.setDateAsStr( self._varData.get())

            self.impreza.kopiuj_z(tmpImpreza)
            if self._nowy:
                self.event.set(self.NEW_IMPREZA)
            else:
                self.event.set(self.UPDATE_IMPREZA)
            self.destroy()
        except Exception as e:
            messagebox.showerror(title="Błąd danych", message=e)

