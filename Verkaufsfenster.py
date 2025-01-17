import tkinter as tk
from tkinter import ttk, messagebox
import time

class Verkaufsfenster(tk.Toplevel):
    def __init__(self, root, getraenkeListe):
        super().__init__(root)
        self.title("Verkaufsfenster")
        self.geometry("400x500")
        self.getraenkeListe = getraenkeListe
        self.eingeworfenes_geld = 0.0
        self.ausgewaehltes_getraenk = None
        self.menge = 1 
        self.gesamtpreis = 0.0

        self.center_window()

        self.getraenke_combobox = ttk.Combobox(self, state="readonly")
        self.getraenke_combobox["values"] = [f"{g.name} - {g.preis} €" for g in self.getraenkeListe]
        self.getraenke_combobox.place(relx=0.5, rely=0.1, relwidth=0.8, anchor="center")
        self.getraenke_combobox.bind("<<ComboboxSelected>>", self.getraenk_auswaehlen)

        self.preis_label = ttk.Label(self, text="Preis: 0,00 €")
        self.preis_label.place(relx=0.5, rely=0.2, anchor="center")

        self.geld_label = ttk.Label(self, text="Eingeworfenes Geld: 0,00 €")
        self.geld_label.place(relx=0.5, rely=0.3, anchor="center")

        self.menge_label = ttk.Label(self, text="Menge:")
        self.menge_label.place(relx=0.5, rely=0.4, anchor="center")

        self.menge_entry = ttk.Entry(self)
        self.menge_entry.place(relx=0.5, rely=0.45, relwidth=0.3, anchor="center")
        self.menge_entry.insert(0, "1")  # Standardwert Menge
        self.menge_entry.bind("<FocusOut>", self.berechne_gesamtpreis)
        self.menge_entry.bind("<Return>", self.berechne_gesamtpreis)

        self.gesamtpreis_label = ttk.Label(self, text="Gesamtpreis: 0,00 €")
        self.gesamtpreis_label.place(relx=0.5, rely=0.5, anchor="center")

        self.muenz_buttons = [0.05, 0.10, 0.20, 0.50, 1.0, 2.0]
        button_x_start = 0.1  
        for i, wert in enumerate(self.muenz_buttons):
            btn = ttk.Button(self, text=f"{wert:.2f} €", command=lambda w=wert: self.geld_einwerfen(w))

            # i * 0.xx Größer = Abstand größer | kleiner = Abstand weniger
            btn.place(relx=button_x_start + i * 0.16, rely=0.55, anchor="center")

        self.kaufen_button = ttk.Button(self, text="Kaufen", command=self.kauf_starten, state="disabled")
        self.kaufen_button.place(relx=0.5, rely=0.65, relwidth=0.8, anchor="center")

        self.ausgabe_label = ttk.Label(self, text="Flaschenausgabe: -")
        self.ausgabe_label.place(relx=0.5, rely=0.8, anchor="center")

    def center_window(self):
        window_width = 400
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    def getraenk_auswaehlen(self, event):
        index = self.getraenke_combobox.current()
        if index != -1:
            self.ausgewaehltes_getraenk = self.getraenkeListe[index]
            self.preis_label.config(text=f"Preis: {self.ausgewaehltes_getraenk.preis:.2f} €")
            self.berechne_gesamtpreis() 
            self.kaufen_button.config(state="normal")

    def berechne_gesamtpreis(self, event=None):
        try:
            self.menge = int(self.menge_entry.get())
            if self.menge < 1:
                self.menge = 1 
                self.menge_entry.delete(0, tk.END)
                self.menge_entry.insert(0, "1")
        except ValueError:
            self.menge = 1  
            self.menge_entry.delete(0, tk.END)
            self.menge_entry.insert(0, "1")

        if self.ausgewaehltes_getraenk:
            self.gesamtpreis = self.ausgewaehltes_getraenk.preis * self.menge
            self.gesamtpreis_label.config(text=f"Gesamtpreis: {self.gesamtpreis:.2f} €")

    def geld_einwerfen(self, betrag):
        self.eingeworfenes_geld += betrag
        self.geld_label.config(text=f"Eingeworfenes Geld: {self.eingeworfenes_geld:.2f} €")

        if self.eingeworfenes_geld >= self.gesamtpreis:
            self.kaufen_button.config(state="normal")

    def kauf_starten(self):

        preis = self.gesamtpreis

        if self.eingeworfenes_geld < preis:
            messagebox.showerror("Fehler", f"Nicht genug Geld! Preis: {preis:.2f} €, Eingeworfen: {self.eingeworfenes_geld:.2f} €")
            return

        wechselgeld = self.eingeworfenes_geld - preis
        self.eingeworfenes_geld = 0  

        self.geld_label.config(text=f"Eingeworfenes Geld: 0,00 €")
        self.ausgabe_label.config(text="Flaschenausgabe: Wird ausgegeben...")

        self.kaufen_button.config(state="disabled")
        
        self.after(0, self.flaschen_ausgeben, wechselgeld)

    def flaschen_ausgeben(self, wechselgeld):
        print(f"Flaschenausgabe | menge: {self.menge}")
        for i in range(1,self.menge+1):
            self.ausgabe_label.config(text=f"Flaschenausgabe | Flaschen menge: {i} |  {self.ausgewaehltes_getraenk.name}")

        self.after(1500, self.ausgabe_label.config, {"text": f"Flaschenausgabe: Fertig! Wechselgeld: {wechselgeld:.2f} €" if wechselgeld > 0 else "Flaschenausgabe: Fertig!"})

