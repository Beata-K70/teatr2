import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox

import BiletDef
import KlientDialog
import ImprezaDialog
import ListaBiletowDialog
import SalaDef
import TeatrDB
import sys

from KlientDef import *
from ImprezaDef import *


class TeatrApp:

    def __init__(self):
        self.statusTab = []

        self.window = tk.Tk()
        # współpraca z okienkami potomnymi
        self.ev_klient = tk.IntVar(master=self.window, name="KlientEvent")
        self.ev_klient.trace("w", self.klient_callback)
        self.ev_impreza = tk.IntVar(master=self.window, name="ImprezaEvent")
        self.ev_impreza.trace("w", self.impreza_callback)
        self.ev_kup_bilet = tk.IntVar(master=self.window, name="KupBiletEvent")
        self.ev_kup_bilet.trace("w", self.kup_bilet_callback)
        self.klient = Klient()
        self.impreza = Impreza()
        self.zakup_biletow = BiletDef.Zakup()

        # tworzenie okna głównego
        self.window.geometry('1024x600')
        self.window.title('Teatr')
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # -- menu ---
        # self._dodaj_glowne_menu(self.window)

        # button_bar
        button_bar = tk.Frame(self.window)  # , background='magenta'  )
        button_bar.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        button_bar.grid_rowconfigure(0, weight=1)
        button_bar.grid_columnconfigure(0, weight=1)
        self._dodaj_szybkie_buttony(button_bar)

        # ---
        self.middle = tk.Frame(self.window)  # background='green')
        self.middle.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.middle.grid_rowconfigure(0, weight=1)
        self.middle.grid_columnconfigure(0, weight=0)

        self.editor1 = tk.Text(self.middle, bg='white')
        self.editor1.grid(row=0, column=0, sticky=tk.NSEW)
        self._build_klient_list_box()
        self._build_impreza_list_box()

        # --- StatusBar -------
        status_bar = tk.Frame(self.window)  # , background='yellow')
        status_bar.grid(row=2, column=0, padx=5, pady=2, columnspan=1, sticky=tk.NSEW)
        status_bar.grid_rowconfigure(0, weight=1)
        status_bar.grid_columnconfigure(0, weight=1)
        self._dadaj_pola_statusu(status_bar)

        # main
        m = sys.version.split()
        self.statusTab[3]['text'] = f'Python: {m[0]}'
        self.window.after(1000, self.timer_update, 0, 10)
        self.reload_list_imprez()
        self.window.mainloop()

    def _dadaj_pola_statusu(self, frame):
        status_w = [(10, "center"), (5, "center"), (15, "w"), (25, "w")]
        idx = 1
        for w in status_w:
            panel = tk.Label(frame, text=idx, width=w[0], anchor=w[1], relief="sunken")
            panel.pack(side=tk.LEFT, padx=2)
            self.statusTab.append(panel)
            idx += 1

    def _dodaj_szybkie_buttony(self, bar):

        tk.Button(bar, text="Lista imprez", fg="blue", command=self.lista_imprez_btn_click).pack(side=tk.LEFT, ipadx=8)
        tk.Button(bar, text="Dodaj impreze", fg="blue", command=self._btn_dodaj_impreza).pack(side=tk.LEFT, ipadx=8)

        tk.Button(bar, text="Lista klientów", fg="blue", command=self.lista_klientow_btn_click).pack(side=tk.LEFT,
                                                                                                     ipadx=8)
        tk.Button(bar, text="Dodaj klient", fg="blue", command=self._btn_dodaj_klient).pack(side=tk.LEFT, padx=4,
                                                                                            ipadx=8)
        # tk.Button(bar, text="Edytor", fg="blue", command=self.edytor_btn_click).pack(side=tk.LEFT, ipadx=8)

    def _dodaj_glowne_menu(self, glowne_okno):
        menu_bar = tk.Menu(glowne_okno)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.make_active)
        file_menu.add_command(label="Open", command=self.make_deactive)
        file_menu.add_command(label="Save", command=self.do_nothing)
        file_menu.add_command(label="Save as...", command=self.do_nothing)
        file_menu.add_command(label="Close", command=self.do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=glowne_okno.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # ----
        klient_menu = tk.Menu(menu_bar, tearoff=0)
        klient_menu.add_command(label="Nowy", command=self.dodaj_klient)
        klient_menu.add_command(label="Edytuj", command=self.app_edytuj_klient)
        menu_bar.add_cascade(label="Klient", menu=klient_menu)

        # ----
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.do_nothing)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="F4", command=self.do_nothing)
        edit_menu.add_command(label="Copy", command=self.do_nothing)
        edit_menu.add_command(label="Paste", command=self.do_nothing)
        edit_menu.add_command(label="Delete", command=self.do_nothing)
        edit_menu.add_command(label="Select All", command=self.do_nothing)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        # ----
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help Index", command=self.do_nothing)
        help_menu.add_command(label="About...", command=self.do_nothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        # ----
        glowne_okno.config(menu=menu_bar)

    # ---------   przełączanie zawartośc Middle ---------------------
    def deaktywuj_wszystkie(self):
        self.middle.grid_columnconfigure(0, weight=1)
        self.editor1.grid_forget()
        self.klient_lista_box.grid_forget()
        self.impreza_lista_box.grid_forget()

    def aktywny_edytor(self):
        self.deaktywuj_wszystkie()
        self.editor1.grid(row=0, column=0, sticky=tk.NSEW)

    def aktywna_lista_klientow(self):
        self.deaktywuj_wszystkie()
        self.klient_lista_box.grid(row=0, column=0, sticky='nswe')

    def aktywna_lista_imprez(self):
        self.deaktywuj_wszystkie()
        self.impreza_lista_box.grid(row=0, column=0, sticky='nswe')

    #  --- edytor --------

    def clear_editor(self):
        self.editor1.delete(1.0, tk.END)

    def add_editor(self, txt):
        self.editor1.insert(tk.INSERT, txt)

    #  --- klient list_box --------

    def handleRightClick_klient_list_box(self, event):
        focused = self.klient_lista_box.focus()
        if focused == "":
            item_state = tk.DISABLED
        else:
            item_state = tk.ACTIVE
        self._klient_context_menu.entryconfigure("Edytuj", state=item_state)
        self._klient_context_menu.entryconfigure("Pokaż bilety", state=item_state)
        self._klient_context_menu.entryconfigure("Usuń", state=item_state)
        self._klient_context_menu.post(event.x_root, event.y_root)

    klient_header = ['id', 'Imię', 'Nazwisko', 'Miejscowość', "Ulica", 'emai', 'telefon']

    def _build_klient_list_box(self):

        self.klient_lista_box = ttk.Treeview(master=self.middle, columns=self.klient_header, show="headings")
        self._klient_context_menu = tk.Menu(self.window, tearoff=0)
        # self._klient_context_menu.add_command(label="Kup bilet", command=self.app_klient_kup_bilet)
        self._klient_context_menu.add_command(label="Pokaż bilety", command=self.app_pokaz_bilety_klienta)
        self._klient_context_menu.add_separator()
        self._klient_context_menu.add_command(label="Edytuj", command=self.app_edytuj_klient)
        self._klient_context_menu.add_command(label="Usuń", command=self.app_usun_klient)

        self.klient_lista_box.bind("<Button-3>", self.handleRightClick_klient_list_box)

        for col in self.klient_header:
            title = col.title()
            self.klient_lista_box.heading(col, text=title)  # , command=lambda c=col: sortby(self.tree, c, 0))
            w = int(1.5 * tkFont.Font().measure(title))
            self.klient_lista_box.column(col, width=w)

    def reload_list_klientow(self):
        self.aktywna_lista_klientow()
        klients = TeatrDB.load_klints()
        self.fill_list_klients(klients)

    def fill_list_klients(self, klients):
        for i in self.klient_lista_box.get_children():
            self.klient_lista_box.delete(i)
        for item in klients:
            self.klient_lista_box.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.klient_lista_box.column(self.klient_header[ix], width=None) < col_w:
                    self.klient_lista_box.column(self.klient_header[ix], width=col_w)

    def get_selected_klient_z_listy(self):
        selected_list = self.klient_lista_box.selection()
        if len(selected_list) > 0:
            selected = selected_list[0]
            child = self.klient_lista_box.item(selected)
            klient_id = child["values"][0]
            return klient_id
        else:
            return -1

    def edytuj_klient(self):
        klient_id = self.get_selected_klient_z_listy()
        if klient_id > 0:
            if TeatrDB.load_klient(klient_id, self.klient):
                KlientDialog.KlientForm(self.window, self.ev_klient, self.klient, False)

    def usun_klient(self):
        klient_id = self.get_selected_klient_z_listy()
        if klient_id > 0:
            tmp_klient = Klient()
            if TeatrDB.load_klient(klient_id, tmp_klient):
                klient_info = f' {tmp_klient.imie} {tmp_klient.nazwisko} '
                txt = f'Czy chcesz usunść klienta {klient_info} ?'
                if messagebox.askyesno(title="Usuwanie klienta", message=txt):
                    if not TeatrDB.delete_klient(tmp_klient.id):
                        messagebox.showinfo(title="Error", message=f'Błąd usunięcia klienta {klient_info} ')
        self.reload_list_klientow()

    def pokaz_bilety_klienta(self):
        klient_id = self.get_selected_klient_z_listy()
        if klient_id > 0:
            lista_biletow = TeatrDB.load_bilety_dla_klienta(klient_id)
            form = ListaBiletowDialog.BiletyKlientaForm(self.window, klient_id)
            form.fill_lista_biletow(lista_biletow)

    def app_klient_kup_bilet(app):
        pass

    def app_pokaz_bilety_klienta(app):
        app.pokaz_bilety_klienta()

    def dodaj_klient(app):
        KlientDialog.KlientForm(app.window, app.ev_klient, app.klient, True)

    def app_edytuj_klient(app):
        app.edytuj_klient()

    def app_usun_klient(app):
        app.usun_klient()

    def klient_callback(*sv):
        app = sv[0]
        ev_val = app.ev_klient.get()
        if ev_val == KlientDialog.KlientForm.NEW_KLIENT:
            TeatrDB.add_klient(app.klient)
            app.reload_list_klientow()
        if ev_val == KlientDialog.KlientForm.UPDATE_KLIENT:
            TeatrDB.update_klient(app.klient)
            app.reload_list_klientow()

    #  --- impreza list_box --------

    def handleRightClick_impreza_list_box(self, event):
        focused = self._impreza_context_menu.focus()
        if focused == "":
            item_state = tk.DISABLED
        else:
            item_state = tk.ACTIVE
        self._impreza_context_menu.entryconfigure("Edytuj", state=item_state)
        self._impreza_context_menu.post(event.x_root, event.y_root)

    imprezy_header = ['id', 'Nazwa', 'Data', 'Sala', "Cena A", "Cena B", "Cena C", "Cena D"]

    def _build_impreza_list_box(self):
        self.impreza_lista_box = ttk.Treeview(master=self.middle, columns=self.imprezy_header, show="headings")

        self._impreza_context_menu = tk.Menu(self.window, tearoff=0, )
        self._impreza_context_menu.add_command(label="Kup bilet na impreze", command=self.app_impreza_kup_bilet)
        self._impreza_context_menu.add_separator()
        self._impreza_context_menu.add_command(label="Pokaż bilety", command=self.app_pokaz_bilety_z_imprezy)
        self._impreza_context_menu.add_command(label="Policz bilety", command=self.app_policz_bilety_z_imprezy)
        self._impreza_context_menu.add_command(label="Policz nie sprzedane bilety",
                                               command=self.app_policz_bilety_z_imprezy_nie_sprzedane)
        self._impreza_context_menu.add_separator()
        self._impreza_context_menu.add_command(label="Edytuj", command=self.app_edytuj_impreza)
        self._impreza_context_menu.add_command(label="Usuń", command=self.app_usun_impreza)

        self.impreza_lista_box.bind("<Button-3>", self.handleRightClick_impreza_list_box)

        for col in self.imprezy_header:
            title = col.title()
            self.impreza_lista_box.heading(col, text=title)  # , command=lambda c=col: sortby(self.tree, c, 0))
            w = int(1.5 * tkFont.Font().measure(title))
            self.impreza_lista_box.column(col, width=w)

    def reload_list_imprez(self):
        self.aktywna_lista_imprez()
        imprezy = TeatrDB.load_imprezy()
        self.fill_list_impreza(imprezy)

    def fill_list_impreza(self, imprezy):
        for i in self.impreza_lista_box.get_children():
            self.impreza_lista_box.delete(i)
        for item in imprezy:
            self.impreza_lista_box.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.impreza_lista_box.column(self.imprezy_header[ix], width=None) < col_w:
                    self.impreza_lista_box.column(self.imprezy_header[ix], width=col_w)

    def get_selected_impreza_z_listy(self):
        selected_list = self.impreza_lista_box.selection()
        if len(selected_list) > 0:
            selected = selected_list[0]
            child = self.impreza_lista_box.item(selected)
            impreza_id = child["values"][0]
            return impreza_id
        else:
            return -1

    def policz_bilety_z_imprezy(self, wszystkie):
        impreza_id = self.get_selected_impreza_z_listy()
        if impreza_id > 0:
            ilosc = TeatrDB.policz_bilety_z_imprezy(impreza_id, wszystkie)
            wynik = TeatrDB.policz_bilety_z_imprezy_dla_kategorii(impreza_id, wszystkie)
            tmp_impreza = Impreza()
            if TeatrDB.load_impreza(impreza_id, tmp_impreza):
                if wszystkie:
                    txt = f'Ilość miejsc: {ilosc}.\n'
                else:
                    txt = f'Ilość nie sprzedanych miejsc: {ilosc}. \n'
                txt = txt + "W tym:\n"
                for x in wynik:
                    txt = txt + f'kategoria "{x[0]}" : {x[1]}\n'

                messagebox.showinfo(title=f'Impreza : {tmp_impreza.nazwa}, data: {tmp_impreza.data}',
                                    message=txt)

    def edytuj_impreza(self):
        impreza_id = self.get_selected_impreza_z_listy()
        if impreza_id > 0:
            if TeatrDB.load_impreza(impreza_id, self.impreza):
                ImprezaDialog.ImprezaForm(self.window, self.ev_impreza, self.impreza, False)

    def usun_impreza(self):
        impreza_id = self.get_selected_impreza_z_listy()
        if impreza_id > 0:
            tmp_impreza = Impreza()
            if TeatrDB.load_impreza(impreza_id, tmp_impreza):
                impreza_info = f' {tmp_impreza.nazwa} z dnia {tmp_impreza.data} '
                txt = f'Czy chcesz usunść imprezę {impreza_info} ?'
                if messagebox.askyesno(title="Usuwanie imprezy", message=txt):
                    TeatrDB.usun_bilety_z_imprezy(impreza_id)
                    if not TeatrDB.usun_impreza(tmp_impreza.id):
                        messagebox.showinfo(title="Error", message=f'Błąd usunięcia imprezy {impreza_info} ')
        self.reload_list_imprez()

    def _konwertuj_liste_biletow(self, lista_biletow):
        nowa_lista = []
        cnt = 0
        for bilet in lista_biletow:  # bilet:  {0}-bilet.kategoria, {1}-bilet.rzad, {2}-bilet.miejsce, {3}-bilet.cena, {4}-klient.name, {5}-klient.forname
            miejsce = f'R{bilet[1]}M{bilet[2]}'
            if bilet[4] != "NULL":
                klient_name = bilet[4] + ' ' + bilet[5]
            else:
                klient_name = '-'
            nowy_bilet = [str(cnt + 1),  # lp
                          bilet[0],  # kategoria
                          miejsce,
                          bilet[3],  # cena
                          klient_name]
            nowa_lista.append(nowy_bilet)
            cnt += 1
        return nowa_lista

    def _konwertuj_liste_biletow_tylko_niesprzedane(self, lista_biletow):
        nowa_lista = []
        cnt = 0
        for bilet in lista_biletow:  # bilet:  {0}-bilet.kategoria, {1}-bilet.rzad, {2}-bilet.miejsce, {3}-bilet.cena, {4}-klient.name, {5}-klient.forname
            if bilet[4] == "NULL":
                nowy_bilet = [str(cnt + 1),  # lp
                              bilet[0],  # kategoria
                              bilet[1],  # rząd
                              bilet[2],  # miejsce
                              bilet[3]]  # cena
                nowa_lista.append(nowy_bilet)
                cnt += 1
        return nowa_lista

    def pokaz_bilety_z_imprezy(self):
        impreza_id = self.get_selected_impreza_z_listy()
        if impreza_id > 0:
            impreza = Impreza()
            TeatrDB.load_impreza(impreza_id, impreza)
            lista_biletow = TeatrDB.load_bilety_dla_imprezy_ex(impreza_id)
            nowa_lista = self._konwertuj_liste_biletow(lista_biletow)
            form = ListaBiletowDialog.ListaBiletowForm(self.window, impreza)
            form.fill_lista_biletow(nowa_lista)

    def impreza_kup_bilet(self):
        impreza_id = self.get_selected_impreza_z_listy()
        if impreza_id > 0:
            impreza = Impreza()
            TeatrDB.load_impreza(impreza_id, impreza)
            lista_biletow = TeatrDB.load_bilety_dla_imprezy_ex(impreza_id)
            nowa_lista = self._konwertuj_liste_biletow_tylko_niesprzedane(lista_biletow)
            if len(nowa_lista) > 0:
                form = ListaBiletowDialog.KupBiletForm(self.window, impreza, self.ev_kup_bilet, self.zakup_biletow)
                form.fill_lista_biletow(nowa_lista)
            else:
                messagebox.showinfo(title=f"Impreza: {impreza.nazwa}", message="Brak biletów")

    def wykonaj_kup_bilet(self):
        print(id(self.zakup_biletow), self.zakup_biletow)
        result = TeatrDB.execute_zakup(self.zakup_biletow)
        print(result)

    def dodaj_impreza(self):
        nazwa_sali = self.impreza.sala;
        sala = SalaDef.Sala(nazwa_sali)
        ilosc_biletow = sala.getj_suma_krzesel()
        txt = f' Czy chcesz dodać imprezę  "{self.impreza.nazwa}" w dnia {self.impreza.data}\n Sala: {self.impreza.sala}, ilość biletów: {ilosc_biletow} ?'
        if messagebox.askyesno(title="Dodawanie imprezy", message=txt):
            TeatrDB.add_impreza(self.impreza)
            lista_krzesel = sala.buduj_lista_krzesel()
            for krzeslo in lista_krzesel:
                bilet = BiletDef.Bilet.daj_wypelniony(krzeslo, self.impreza)
                TeatrDB.dodaj_bilet(bilet)
            self.reload_list_imprez()

    def app_policz_bilety_z_imprezy(app):
        app.policz_bilety_z_imprezy(True)

    def app_policz_bilety_z_imprezy_nie_sprzedane(app):
        app.policz_bilety_z_imprezy(False)

    def app_edytuj_impreza(app):
        app.edytuj_impreza()

    def app_usun_impreza(app):
        app.usun_impreza()

    def app_pokaz_bilety_z_imprezy(app):
        app.pokaz_bilety_z_imprezy()

    def app_impreza_kup_bilet(app):
        app.impreza_kup_bilet()

    def impreza_callback(*sv):
        app = sv[0]
        ev_val = app.ev_impreza.get()
        if ev_val == ImprezaDialog.ImprezaForm.NEW_IMPREZA:
            app.dodaj_impreza()
        if ev_val == ImprezaDialog.ImprezaForm.UPDATE_IMPREZA:
            TeatrDB.update_impreza(app.impreza)
            app.reload_list_imprez()

    def kup_bilet_callback(*sv):
        app = sv[0]
        app.wykonaj_kup_bilet()

    # ----------------------------------------------------------

    def make_active(app):
        app.redbutton.config(state="active")

    def make_deactive(app):
        app.redbutton.config(state="disabled")

    def do_nothing(app):
        print(type(app))

    def test_fun(self, print_fun):
        print_fun('To jest text\n')

    def _btn_dodaj_klient(app):
        KlientDialog.KlientForm(app.window, app.ev_klient, app.klient, True)

    def _btn_dodaj_impreza(app):
        ImprezaDialog.ImprezaForm(app.window, app.ev_impreza, app.impreza, True)

    # -- Klient --------------------------------

    def lista_klientow_btn_click(app):
        app.reload_list_klientow()

    def lista_imprez_btn_click(app):
        app.reload_list_imprez()

    def edytor_btn_click(app):
        app.aktywny_edytor()

    def timer_update(app, b, c):
        app.window.after(1000, app.timer_update, 0, 10)
        tm = datetime.now()
        txt = tm.strftime("%H:%M:%S")
        app.statusTab[0]['text'] = txt


# ---------------
TeatrDB.init()
TeatrApp()
