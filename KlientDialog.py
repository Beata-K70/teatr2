from tkinter import *
from BaseDialog import *
from KlientDef import *
from tkinter import messagebox


class KlientForm(BaseForm):
    NEW_KLIENT = 101
    UPDATE_KLIENT = 102

    def __init__(self, parent, event, klient, nowy=True):

        self.klient = klient
        self.event = event
        self._nowy = nowy

        # zmienne
        self._varImie = tk.StringVar()
        self._varNazwisko = tk.StringVar()
        self._varMiejscowosc = tk.StringVar()
        self._varAdres = tk.StringVar()
        self._varAdres = tk.StringVar()
        self._varEmail = tk.StringVar()
        self._varTelefon = tk.StringVar()

        super().__init__(parent, "wao")
        if self._nowy:
            self.title('Nowy klient')
        else:
            self.title('Edytuj klienta')

        if not nowy:
            self._set_klient(klient)

    def _get_form_size(self):
        return [320, 200]  # width x height

    # metoda wywoływana z obiektu przodka, gdy już jest gotowy układ ramek
    def _add_edit_items(self, frame):
        imie_edit = self._add_edit_item(frame, "Imię", self._varImie)
        nazwisko_edit = self._add_edit_item(frame, "Nawisko", self._varNazwisko)
        if not self._nowy:
            imie_edit.config(state="disabled")
            nazwisko_edit.config(state="disabled")
        self._add_edit_item(frame, "Miejscowość", self._varMiejscowosc)
        self._add_edit_item(frame, "Adres", self._varAdres)
        self._add_edit_item(frame, "email", self._varEmail)
        self._add_edit_item(frame, "telefon", self._varTelefon)

    def _clear_btn_click(self):
        self._varImie.set("")
        self._varNazwisko.set("")
        self._varMiejscowosc.set("")
        self._varAdres.set("")
        self._varEmail.set("")
        self._varTelefon.set("")

    def _set_klient(self, klient):
        self._varImie.set(klient.imie)
        self._varNazwisko.set(klient.nazwisko)
        self._varMiejscowosc.set(klient.miejscowosc)
        self._varAdres.set(klient.adres)
        self._varEmail.set(klient.email)
        self._varTelefon.set(klient.telefon)

    def _ok_btn_click(self):
        tmpKlient = Klient()
        try:
            # najpierw do obiektu tymczasowego aby sprawdzić czy dane są ok
            tmpKlient.id = self.klient.id
            tmpKlient.imie = self._varImie.get()
            tmpKlient.nazwisko = self._varNazwisko.get()
            tmpKlient.miejscowosc = self._varMiejscowosc.get()
            tmpKlient.adres = self._varAdres.get()
            tmpKlient.email = self._varEmail.get()
            tmpKlient.telefon = self._varTelefon.get()

            self.klient.kopiuj_z(tmpKlient)
            if self._nowy:
                self.event.set(self.NEW_KLIENT)
            else:
                self.event.set(self.UPDATE_KLIENT)
            self.destroy()
        except Exception as e:
            messagebox.showerror(title="Błąd danych", message=e)
