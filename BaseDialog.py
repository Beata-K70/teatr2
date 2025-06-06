import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class BaseForm(tk.Toplevel):
    def __init__(self, parent, buttons="wao", top_most=True, resizable=False):
        super().__init__(parent)  # *args, **kwargs)

        self._set_center_position(parent)
        if top_most:
            self.attributes('-topmost', 'true')
        self.resizable(resizable, resizable)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.positionfrom()

        self._create_widgets(buttons)

    def _create_widgets(self, buttons):
        self.middle = tk.Frame(self) # background='silver')
        self.middle.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.middle.grid_columnconfigure(0, weight=1)
        self.middle.grid_rowconfigure(0, weight=0)

        bottom_fr = tk.Frame(self)  # , background='yellow')
        bottom_fr.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky=tk.NSEW)
        bottom_fr.grid_rowconfigure(0, weight=1)
        bottom_fr.grid_columnconfigure(0, weight=0)

        # ---
        self._add_edit_items(self.middle)
        # ---
        if 'o' in buttons:
            ok_btn = tk.Button(bottom_fr, text="OK", command=self._ok_btn_click)
            ok_btn.pack(side=tk.RIGHT, padx=5) #ukladanie buttonow od prawej
        if 'a' in buttons:
            anuluj_btn = tk.Button(bottom_fr, text="Anuluj", command=self._anuluj_btn_click)
            anuluj_btn.pack(side=tk.RIGHT, padx=5)
        if 'w' in buttons:
            clear_btn = tk.Button(bottom_fr, text="Wyczyść", command=self._clear_btn_click)
            clear_btn.pack(side=tk.RIGHT, padx=5)

    def _add_edit_item(self, parent, caption, var):
        item_fr = tk.Frame(parent)  # , background='blue')
        item_fr.grid(sticky=tk.EW)
        label = tk.Label(item_fr, text=caption + ':', width=14, anchor="e")
        label.pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(item_fr, width=30, textvariable=var)
        entry.pack(side=tk.LEFT, padx=5)
        return entry

    def _add_combobox_item(self, parent, caption, item_list, var):
        item_fr = tk.Frame(parent)  # , background='blue')
        item_fr.grid(sticky=tk.EW)
        label = tk.Label(item_fr, text=caption + ':', width=14, anchor="e")
        label.pack(side=tk.LEFT, padx=5)
        combo = ttk.Combobox(item_fr, width=30, textvariable=var, state="readonly", values=item_list)
        combo.pack(side=tk.LEFT, padx=5)
        return combo

    def _add_list(self, parent, headers):
        lista_box = ttk.Treeview(master=parent, columns=headers, show="headings")
        lista_box.grid(sticky=tk.NSEW)
        for col in headers:
            title = col.title()
            lista_box.heading(col, text=title)
            w = int(1.5 * tkFont.Font().measure(title))
            lista_box.column(col, width=w)
        return lista_box

    def _set_center_position(self, main_w):
        x = main_w.winfo_x()
        y = main_w.winfo_y()
        w = main_w.winfo_width()
        h = main_w.winfo_height()

        [form_w, form_h] = self._get_form_size();

        self.geometry("+%d+%d" % (x + (w - form_w) / 2, y + (h - form_h) / 2))
        self.geometry(f'{form_w}x{form_h}')

    def _anuluj_btn_click(self):
        self.destroy()

    def _clear_btn_click(self):
        pass

    def _add_edit_items(self, frame):
        pass

    def _get_form_size(self):
        pass

    def _ok_btn_click(self):
        pass
