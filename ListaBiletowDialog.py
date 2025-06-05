from tkinter import *

import KlientDef
from BaseDialog import *
import tkinter.font as tkFont
import TeatrDB

from BiletDef import *
from tkinter import messagebox


class ListaBiletowForm(BaseForm):

    def __init__(self, parent, impreza):
        self.impreza = impreza
        self._list_box = None

        super().__init__(parent, buttons="o", top_most=False, resizable=True)

        self.title(f'Lista biletów:{impreza.nazwa} w dniu {impreza.data}')

    def _get_form_size(self):
        return [480, 400]  # width x height

    def _clear_btn_click(self):
        pass

    bilety_header = ['lp', 'Kategoria', 'Miejsce', 'Cena', "Klient"]

    def _add_edit_items(self, frame):
        self._list_box = self._add_list(frame, self.bilety_header)
        frame.grid_rowconfigure(0, weight=1)

    def fill_lista_biletow(self, tickets):
        # czyszczenie starych
        for i in self._list_box.get_children():
            self._list_box.delete(i)
        # wypelnianie
        for item in tickets:
            self._list_box.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self._list_box.column(self.bilety_header[ix], width=None) < col_w:
                    self._list_box.column(self.bilety_header[ix], width=col_w)

    def _ok_btn_click(self):
        self.destroy()


# ---------------------------------

class KupBiletForm(BaseForm):

    def __init__(self, parent, impreza, event, kupione_bilety):
        self.impreza = impreza
        self.event = event
        self._list_box = None
        self.zakup = kupione_bilety

        self._varKlient = tk.StringVar()

        super().__init__(parent, buttons="ao", top_most=False, resizable=True)
        self.title(f'Lista biletów:{impreza.nazwa} w dniu {impreza.data}')

    def _get_form_size(self):
        return [480, 400]  # width x height

    def _clear_btn_click(self):
        pass

    bilety_header = ['lp', 'Kategoria', 'Rząd', 'Miejsce', 'Cena']

    def _add_edit_items(self, frame):
        lista_klientow = TeatrDB.load_klients_human_mode()
        combo = self._add_combobox_item(frame, "Klient:", lista_klientow, self._varKlient)
        combo.pack(side=tk.LEFT, pady=10)
        self._list_box = self._add_list(frame, self.bilety_header)
        frame.grid_rowconfigure(1, weight=1)

    def fill_lista_biletow(self, tickets):

        # czyszczenie starych
        for i in self._list_box.get_children():
            self._list_box.delete(i)
        # wypelnianie
        for item in tickets:
            self._list_box.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self._list_box.column(self.bilety_header[ix], width=None) < col_w:
                    self._list_box.column(self.bilety_header[ix], width=col_w)

    def _ok_btn_click(self):
        self.zakup.impreza_id = self.impreza.id
        self.zakup.klient_nazwa = self._varKlient.get()
        if self.zakup.klient_nazwa != "":
            self.zakup.klient_id = TeatrDB.get_klient_id_by_human_name(self.zakup.klient_nazwa)
            selected_list = self._list_box.selection()
            self.zakup.lista = []
            for item in selected_list:
                child = self._list_box.item(item)
                miejsce = [child["values"][2], child["values"][3]]
                self.zakup.lista.append(miejsce)
            # print(id(self.kupione_bilety), self.kupione_bilety)
            self.event.set(1)
            self.destroy()
        else:
            messagebox.showerror(title="Błąd", message="Wybierz klienta")


# ---------------------------------

class BiletyKlientaForm(BaseForm):

    def __init__(self, parent, klient_id):

        super().__init__(parent, buttons="o", top_most=False, resizable=True)
        klient = KlientDef.Klient()
        TeatrDB.load_klient(klient_id, klient)
        self.title(f'Lista biletów klienta: {klient.imie} {klient.nazwisko}')

    def _get_form_size(self):
        return [480, 400]  # width x height

    def _clear_btn_click(self):
        pass

    bilety_header = ['lp', 'Impreza', "Data", 'Miejsce', 'Cena']

    def _add_edit_items(self, frame):
        self._list_box = self._add_list(frame, self.bilety_header)
        frame.grid_rowconfigure(0, weight=1)

    def fill_lista_biletow(self, tickets):

        # czyszczenie starych
        for i in self._list_box.get_children():
            self._list_box.delete(i)
        # wypelnianie
        for item in tickets:
            self._list_box.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self._list_box.column(self.bilety_header[ix], width=None) < col_w:
                    self._list_box.column(self.bilety_header[ix], width=col_w)

    def _ok_btn_click(self):
        self.destroy()
