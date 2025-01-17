import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from threading import Thread

class Verkaufsfenster(tk.Toplevel):
    def __init__(self, root, getraenkeListe):
        super().__init__(root)
        self.title("Verkaufsfenster")
        self.geometry("400x400")
        self.getraenkeListe = getraenkeListe
        self.eingeworfenes_geld = 0.0
        self.ausgewaehltes_getraenk = None

        # Dropdown
        self.getraenke_combobox = ttk.Combobox(self, state="readonly")
        self.getraenke_combobox["values"] = [f"{g.name} - {g.preis} €" for g in self.getraenkeListe]
        self.getraenke_combobox.pack(pady=10)
        self.getraenke_combobox.bind("<<ComboboxSelected>>", self.getraenk_auswaehlen)

        # Preis Label
        self.preis_label = ttk.Label(self, text="Preis: 0,00 €")
        self.preis_label.pack(pady=5)

        # Eingeworfenes Geld Label
        self.geld_label = ttk.Label(self, text="Eingeworfenes Geld: 0,00 €")
        self.geld_label.pack(pady=5)

        # Münzen Buttons
        self.muenz_buttons = [0.05, 0.10, 0.20, 0.50, 1.0, 2.0]
        for wert in self.muenz_buttons:
            btn = ttk.Button(self, text=f"{wert:.2f} €", command=lambda w=wert: self.geld_einwerfen(w))
            btn.pack(side="left", padx=5)

        # Kauf-Button
        self.kaufen_button = ttk.Button(self, text="Kaufen", command=self.kauf_starten, state="disabled")
        self.kaufen_button.pack(pady=10)

        # Ausgabe Label
        self.ausgabe_label = ttk.Label(self, text="Flaschenausgabe: -")
        self.ausgabe_label.pack(pady=10)

    def getraenk_auswaehlen(self, event):
        """Wird ausgelöst, wenn ein Getränk ausgewählt wird."""
        index = self.getraenke_combobox.current()  # Index der Combobox-Auswahl
        if index != -1:  # Sicherstellen, dass ein Getränk ausgewählt wurde
            self.ausgewaehltes_getraenk = self.getraenkeListe[index]
            self.preis_label.config(text=f"Preis: {self.ausgewaehltes_getraenk.preis:.2f} €")
            self.kaufen_button.config(state="normal")

    def geld_einwerfen(self, betrag):
        """Geld einwerfen und automatisch prüfen, ob der Kauf möglich ist."""
        self.eingeworfenes_geld += betrag
        self.geld_label.config(text=f"Eingeworfenes Geld: {self.eingeworfenes_geld:.2f} €")

        # Automatische Kaufprüfung
        if self.ausgewaehltes_getraenk and self.eingeworfenes_geld >= self.ausgewaehltes_getraenk.preis:
            self.kauf_starten()

    def kauf_starten(self):
        """Startet den Kaufprozess, falls genügend Geld eingeworfen wurde."""
        if not self.ausgewaehltes_getraenk:
            messagebox.showerror("Fehler", "Kein Getränk ausgewählt!")
            return

        preis = self.ausgewaehltes_getraenk.preis

        if self.eingeworfenes_geld < preis:
            messagebox.showerror("Fehler", f"Nicht genug Geld! Preis: {preis:.2f} €, Eingeworfen: {self.eingeworfenes_geld:.2f} €")
            return

        # Wechselgeld berechnen
        wechselgeld = self.eingeworfenes_geld - preis
        self.eingeworfenes_geld = 0  # Guthaben zurücksetzen

        # Labels aktualisieren
        self.geld_label.config(text=f"Eingeworfenes Geld: 0,00 €")
        self.ausgabe_label.config(text="Flaschenausgabe: Wird ausgegeben...")

        # Kauf-Button deaktivieren
        self.kaufen_button.config(state="disabled")

        # Simuliere die Flaschenausgabe im Haupt-Thread
        self.after(0, self.flaschen_ausgeben, wechselgeld)

    def flaschen_ausgeben(self, wechselgeld):
        """Simuliert die Ausgabe des Getränks und zeigt Wechselgeld an."""
        time.sleep(1)  # Simuliere eine kleine Wartezeit für die Flaschenausgabe

        # Aktualisieren der Ausgabe-Label
        self.ausgabe_label.config(text=f"Flaschenausgabe: {self.ausgewaehltes_getraenk.name}")
        self.after(1500, self.ausgabe_label.config, {"text": f"Flaschenausgabe: Fertig! Wechselgeld: {wechselgeld:.2f} €" if wechselgeld > 0 else "Flaschenausgabe: Fertig!"})

