import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox

import KlientDialog
import ImprezaDialog
import TeatrDB

from KlientDef import *
from ImprezaDef import *


class TeatrApp:

    def __init__(self):
        self.counter = 0
        self.statusTab = []

        self.window = tk.Tk()
        self.evKlient = tk.IntVar(master=self.window, name="KlientEvent")
        self.evKlient.trace("w", self.klientCallback)
        self.evImpreza = tk.IntVar(master=self.window, name="ImprezaEvent")
        self.evImpreza.trace("w", self.imprezaCallback)

        self.klient = Klient()
        self.impreza = Impreza()

        self.window.geometry('1024x600')
        self.window.title('Teatr')
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # -- menu ---
        self._dodaj_glowne_menu(self.window)

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
        self.klient_lista_box = ttk.Treeview(master=self.middle, columns=self.klient_header, show="headings")
        self._add_klient_list_box()
        self.impreza_lista_box = ttk.Treeview(master=self.middle, columns=self.klient_header, show="headings")
        self._add_impreza_list_box()

        # --- StatusBar -------
        status_bar = tk.Frame(self.window)  # , background='yellow')
        status_bar.grid(row=2, column=0, padx=5, pady=2, columnspan=1, sticky=tk.NSEW)
        status_bar.grid_rowconfigure(0, weight=1)
        status_bar.grid_columnconfigure(0, weight=1)
        self._dadaj_pola_statusu(status_bar)

        # main
        self.window.mainloop()

    klient_header = ['id', 'Imię', 'Nazwisko', 'Miejscowość', "Ulica", 'emai', 'telefon']
    imprezy_header = ['id', 'Nazwa', 'Data', 'Sala', "Cena A", "Cena B", "Cena C", "Cena D"]

    def _dadaj_pola_statusu(self, frame):
        status_w = [(10, "w"), (5, "center"), (15, "w"), (25, "w")]
        idx = 1
        for w in status_w:
            panel = tk.Label(frame, text=idx, width=w[0], anchor=w[1], relief="sunken")
            panel.pack(side=tk.LEFT, padx=2)
            self.statusTab.append(panel)
            idx += 1

    def _dodaj_szybkie_buttony(self, bar):
        self.redbutton = tk.Button(bar, text="Kup bilet", fg="red", command=self._kup_bilet_btn_click)
        self.redbutton.pack(side=tk.LEFT, ipadx=0)

        greenbutton = tk.Button(bar, text="Green", fg="green", command=self._btn_cmd_green)
        greenbutton.pack(side=tk.LEFT, ipadx=0)

        KlientBnt = tk.Button(bar, text="Dodaj klient", fg="blue", command=self._btn_klient)
        KlientBnt.pack(side=tk.LEFT, ipadx=0)

        ImprezaBnt = tk.Button(bar, text="Impreza", fg="blue", command=self._btn_impreza)
        ImprezaBnt.pack(side=tk.LEFT, ipadx=0)

        tk.Button(bar, text="Lista klientów", fg="blue", command=self.lista_btn_click).pack(side=tk.LEFT, ipadx=2)
        tk.Button(bar, text="Edytor", fg="blue", command=self.edytor_btn_click).pack(side=tk.LEFT, ipadx=2)

        tk.Button(bar, text="Message", fg="blue", command=self.btn_message_click).pack(side=tk.LEFT, ipadx=2)

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
        klient_menu.add_command(label="Edytuj", command=self.lista_edytuj_klient)
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
        self.deaktywuj_wszystkie();
        self.editor1.grid(row=0, column=0, sticky=tk.NSEW)

    def aktywna_lista_klientow(self):
        self.deaktywuj_wszystkie();
        self.klient_lista_box.grid(row=0, column=0, sticky='nswe')

    def aktywna_lista_imprez(self):
        self.deaktywuj_wszystkie();
        self.klient_lista_box.grid(row=0, column=0, sticky='nswe')

    #  --- edytor --------

    def clear_editor(self):
        self.editor1.delete(1.0, tk.END)

    def add_editor(self, txt):
        self.editor1.insert(tk.INSERT, txt)

    #  --- klient list_box --------

    def reload_list_klientow(self):
        self.aktywna_lista_klientow()
        klients = TeatrDB.load_klints()
        self.fill_list_klients(klients)

    def handleRightClick_klient_list_box(self, event):
        focused = self.klient_lista_box.focus()
        if focused == "":
            item_state = tk.DISABLED
        else:
            item_state = tk.ACTIVE
        self._klient_context_menu.entryconfigure("Edytuj", state=item_state)
        self._klient_context_menu.post(event.x_root, event.y_root)

    def _add_klient_list_box(self):
        self._klient_context_menu = tk.Menu(self.window, tearoff=0, )
        self._klient_context_menu.add_command(label="Kup bilet", command=self.lista_kup_bilet)
        self._klient_context_menu.add_command(label="Pokaż bilety", command=self.lista_pokaz_bilety_klienta)
        self._klient_context_menu.add_separator()
        self._klient_context_menu.add_command(label="Edytuj", command=self.lista_edytuj_klient)
        self._klient_context_menu.add_command(label="Usuń", command=self.lista_usun_klient)

        self.klient_lista_box.bind("<Button-3>", self.handleRightClick_klient_list_box)

        for col in self.klient_header:
            title = col.title()
            self.klient_lista_box.heading(col, text=title)  # , command=lambda c=col: sortby(self.tree, c, 0))
            w = int(1.5 * tkFont.Font().measure(title))
            self.klient_lista_box.column(col, width=w)

    def fill_list_klients(self, klients):
        for i in self.klient_lista_box.get_children():
            self.klient_lista_box.delete(i)
        for item in klients:
            self.klient_lista_box.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.klient_lista_box.column(self.klient_header[ix], width=None) < col_w:
                    self.klient_lista_box.column(self.klient_header[ix], width=col_w)

    #  --- impreza list_box --------
    def reload_list_imprez(self):
        self.aktywna_lista_imprez()
        imprezy = TeatrDB.load_imprezy()
        self.fill_list_impreza(imprezy)

    def handleRightClick_impreza_list_box(self, event):
        focused = self._impreza_context_menu.focus()
        if focused == "":
            item_state = tk.DISABLED
        else:
            item_state = tk.ACTIVE
        self._klient_context_menu.entryconfigure("Edytuj", state=item_state)
        self._klient_context_menu.post(event.x_root, event.y_root)

    def _add_impreza_list_box(self):
        self._impreza_context_menu = tk.Menu(self.window, tearoff=0, )
        self._impreza_context_menu.add_command(label="Kup bilet", command=self.lista_kup_bilet)
        self._impreza_context_menu.add_command(label="Pokaż bilety", command=self.lista_pokaz_bilety_klienta)
        self._impreza_context_menu.add_separator()
        self._impreza_context_menu.add_command(label="Edytuj", command=self.lista_edytuj_impreza)
        self._impreza_context_menu.add_command(label="Usuń", command=self.lista_usun_impreza)

        self.impreza_lista_box.bind("<Button-3>", self.handleRightClick_impreza_list_box)

        for col in self.klient_header:
            title = col.title()
            self.impreza_lista_box.heading(col, text=title)  # , command=lambda c=col: sortby(self.tree, c, 0))
            w = int(1.5 * tkFont.Font().measure(title))
            self.impreza_lista_box.column(col, width=w)

    def fill_list_impreza(self, imprezy):
        for i in self.klient_lista_box.get_children():
            self.klient_lista_box.delete(i)
        for item in imprezy:
            self.klient_lista_box.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.impreza_lista_box.column(self.klient_header[ix], width=None) < col_w:
                    self.impreza_lista_box.column(self.klient_header[ix], width=col_w)


    def klientCallback(*sv):
        app = sv[0]
        ev_val = app.evKlient.get()
        if ev_val == KlientDialog.KlientForm.NEW_KLIENT:
            TeatrDB.add_klient(app.klient)
            app.reload_list_klientow()
        if ev_val == KlientDialog.KlientForm.UPDATE_KLIENT:
            TeatrDB.update_klient(app.klient)
            app.reload_list_klientow()

    def imprezaCallback(*sv):
        app = sv[0]
        ev_val = app.evImpreza.get()
        if ev_val == ImprezaDialog.ImprezaForm.NEW_IMPREZA:
            TeatrDB.add_impreza(app.impreza)
        if ev_val == ImprezaDialog.ImprezaForm.UPDATE_IMPREZA:
            pass


    def make_active(app):
        app.redbutton.config(state="active")

    def make_deactive(app):
        app.redbutton.config(state="disabled")

    def do_nothing(app):
        print(type(app))

    def _kup_bilet_btn_click(app):
        app.clear_editor()
        # msize = app.editor1.count("1.0", tk.INSERT)
        # app.editor1.insert(tk.INSERT, f'Red Btn size = [{msize[0]}]\n')
        app.statusTab[0]["text"] = "RED"

    def _btn_cmd_green(app):
        app.add_editor(f'Green Btn {app.counter}\n')
        app.counter += 1
        app.statusTab[0]["text"] = "GREEN"
        print(type(app.add_editor))
        print(app.add_editor)
        app.test_fun(app.add_editor)

    def test_fun(self, print_fun):
        print_fun('To jest text\n')

    def _btn_klient(app):
        KlientDialog.KlientForm(app.window, app.evKlient, app.klient, True)

    def _btn_impreza(app):
        ImprezaDialog.ImprezaForm(app.window, app.evImpreza, app.impreza, True)

    # -- Klient --------------------------------
    def dodaj_klient(app):
        KlientDialog.KlientForm(app.window, app.evKlient, app.klient, True)

    def lista_kup_bilet(app):
        pass

    def get_selected_klient_z_listy(self):
        selected_list = self.klient_lista_box.selection()
        if len(selected_list) > 0:
            selected = selected_list[0]
            child = self.klient_lista_box.item(selected)
            klient_id = child["values"][0]
            return klient_id
        else:
            return -1

    def lista_edytuj_klient(app):
        klient_id = app.get_selected_klient_z_listy()
        if klient_id > 0:
            if TeatrDB.load_klient(klient_id, app.klient):
                KlientDialog.KlientForm(app.window, app.evKlient, app.klient, False)

    def lista_usun_klient(app):
        klient_id = app.get_selected_klient_z_listy()
        if klient_id > 0:
            tmp_klient = Klient()
            if TeatrDB.load_klient(klient_id, tmp_klient):
                klient_info = f' {tmp_klient.imie} {tmp_klient.nazwisko} '
                txt = f'Czy chcesz usunść klienta {klient_info} ?'
                if messagebox.askyesno(title="Usuwanie klienta", message=txt):
                    if not TeatrDB.delete_klient(tmp_klient.id):
                        messagebox.showinfo(title="Error", message=f'Błąd usunięcia klienta {klient_info} ')
        app.reload_list_klientow()

    def lista_pokaz_bilety_klienta(app):
        pass

    def lista_btn_click(app):
        app.reload_list_klientow()

    def edytor_btn_click(app):
        app.aktywny_edytor()

    def btn_message_click(app):
        # messagebox.showinfo(title="Informatio", message = "Pierwszy message")
        if messagebox.askokcancel(title="Pytanie", message="Zamknąc okno"):
            print("Zamknąc")


# ---------------
TeatrDB.init()
TeatrApp()
