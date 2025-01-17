from asyncio.windows_events import NULL
from queue import Empty
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import Verkaufsfenster as VK
from Getraenk import Getraenk

class Automat():
    def __init__(self, root):
        self.getraenkeListe = []
        self.anzahlGetraenke = 0

        self.root = root
        self.root.title("Getränkeautomat VendoPy")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        self.getraenke_einlesen()

        if not self.getraenkeListe:
            print("Interne Getränkeliste ist leer")

        self.label_MenuText_Top = ttk.Label(
            self.root,
            text="    Willkommen im PyAutomat\n bitte wählen Sie eine Sorte aus.",
            font=("Segoe UI", 16, "bold")
        )
        self.label_TextGetraenke = ttk.Label(
            self.root,
            text=f"Anzahl der Getränke im Sortiment: {self.anzahlGetraenke}",
            font=("Segoe UI", 16, "bold")
        )

        self.btnSortiment = ttk.Button(self.root, text="Sortiment", command=self.openSortiment)
        self.btnVerkauf = ttk.Button(self.root, text="Getränke Verkauf starten", command=self.openVending)

        self.btnVerkauf.place(relx=0.5, rely=0.6, anchor="s")
        self.btnSortiment.place(relx=0.5, rely=0.4, anchor="s")
        self.label_TextGetraenke.place(relx=0.5, rely=0.2, anchor="s")
        self.label_MenuText_Top.place(relx=0.5, rely=0.0, anchor="n")

    def getraenke_einlesen(self):
        print("Suche nach Produktdatei...")
        try:
            with open("GetränkeListe.txt", "r", encoding="utf-8") as file:
                print("GetränkeListe gefunden.")
                for zeile in file:
                    daten = zeile.strip().split()
                    if len(daten) >= 5:
                        name = " ".join(daten[:-4])
                        preis = float(daten[-4])
                        menge = float(daten[-3])
                        verpackung = daten[-2]
                        alkoholgehalt = daten[-1]
                        getraenk = Getraenk(name, preis, menge, verpackung, alkoholgehalt)
                        self.getraenkeListe.append(getraenk)
                        self.anzahlGetraenke += 1
        except FileNotFoundError:
            print("Datei nicht gefunden")
        except Exception as e:
            print(f"Ein Fehler beim Verarbeiten der Daten ist aufgetreten: {e}")

    def getraenke_speichern(self):
        with open("GetränkeListe.txt", "w", encoding="utf-8") as file:      # UTF - 8 extra mit angeben, wegen vs (:
            for getraenk in self.getraenkeListe:
                print(f"Alkoholgehalt vor dem Speichern: {getraenk.alkoholgehalt}")
                file.write(f"{getraenk.name} {getraenk.preis} {getraenk.menge} {getraenk.verpackung} {getraenk.alkoholgehalt}\n")

    def openSortiment(self):
        for child in self.root.winfo_children():
            if isinstance(child, tk.Toplevel) and child.title() == "Sortiment":
                print("Das Fenster 'Sortiment' ist bereits geöffnet.")
                return

        fenster_breite = 1000
        fenster_hoehe = 350

        sortiment_fenster = tk.Toplevel(self.root)
        sortiment_fenster.title("Sortiment")
        main_fenster_breite = self.root.winfo_width()
        main_fenster_hoehe = self.root.winfo_height()

        # Position des Hauptfensters
        main_fenster_x = self.root.winfo_x()
        main_fenster_y = self.root.winfo_y()

        # Berechnung Fensterposition "Parent" Mitte
        position_x = main_fenster_x + (main_fenster_breite // 2) - (fenster_breite // 2)
        position_y = main_fenster_y + (main_fenster_hoehe // 2) - (fenster_hoehe // 2)
        sortiment_fenster.geometry(f"{fenster_breite}x{fenster_hoehe}+{position_x}+{position_y}")

        label_Text = ttk.Label(
            sortiment_fenster,
            text="Sortiment Übersicht",
            font=("Segoe UI", 16, "bold")
        )
        label_Text.pack()

        tree = ttk.Treeview(
            sortiment_fenster,
            columns=("Name", "Preis", "Menge", "Verpackung", "Alkoholgehalt"),
            show="headings"
        )
        tree.heading("Name", text="Name")
        tree.heading("Preis", text="Preis (€)")
        tree.heading("Menge", text="Menge (ml)")
        tree.heading("Verpackung", text="Verpackung")
        tree.heading("Alkoholgehalt", text="Alkoholgehalt (%)")

        for i, getraenk in enumerate(self.getraenkeListe):
            tree.insert("", "end", iid=i, values=(getraenk.name, getraenk.preis, getraenk.menge, getraenk.verpackung, getraenk.alkoholgehalt))

        tree.pack(fill="both", expand=True)

        def neues_getraenk_hinzufuegen():
            name = simpledialog.askstring("Neues Getränk", "Name des Getränks:")
            if not name:
                return

            try:
                preis = simpledialog.askfloat("Neues Getränk", "Preis in €:")
                menge = simpledialog.askfloat("Neues Getränk", "Menge in ml:")
                verpackung = simpledialog.askstring("Neues Getränk", "Verpackungsart:")
                alkoholgehalt = simpledialog.askfloat("Neues Getränk", "Alkoholgehalt in %:")

                if None in (preis, menge, verpackung, alkoholgehalt):
                    print("Abgebrochen, unvollständige Angaben.")
                    return

                neues_getraenk = Getraenk(name, preis, menge, verpackung, alkoholgehalt)
                self.getraenkeListe.append(neues_getraenk)
                self.anzahlGetraenke += 1
                self.label_TextGetraenke.config(text=f"Anzahl der Getränke im Sortiment: {self.anzahlGetraenke}")

                tree.insert("", "end", iid=len(self.getraenkeListe) - 1, values=(name, preis, menge, verpackung, alkoholgehalt))
                self.getraenke_speichern()
                print(f"Neues Getränk '{name}' hinzugefügt.")
            except Exception as e:
                print(f"Fehler beim Hinzufügen des Getränks: {e}")

        btnNeuesGetraenk = ttk.Button(sortiment_fenster, text="Neues Getränk hinzufügen", command=neues_getraenk_hinzufuegen)
        btnNeuesGetraenk.pack(pady=10)

        def on_edit(event):
            selected_item = tree.selection()
    
            if selected_item:
                pass
                #item_text = tree.item(selected_item[0])['text']
            else:
                print("Kein Element ausgewählt.")
                return
            selected_item = tree.selection()[0]  
            item_values = tree.item(selected_item)["values"]  
            column = tree.identify_column(event.x)  
            column_index = int(column.split('#')[1]) - 1  
            getraenk = self.getraenkeListe[int(selected_item)]  

            alter_wert = None

            if column_index == 0:  
                neuerWert = simpledialog.askstring("Bearbeiten", "Neuer Name:", initialvalue=item_values[column_index])
                if neuerWert:
                    alter_wert = getraenk.name
                    getraenk.name = neuerWert
            elif column_index == 1:
                neuerWert = simpledialog.askfloat("Bearbeiten", "Neuer Preis:", initialvalue=item_values[column_index])
                if neuerWert:
                    alter_wert = getraenk.preis
                    getraenk.preis = neuerWert
            elif column_index == 2:
                neuerWert = simpledialog.askfloat("Bearbeiten", "Neue Menge:", initialvalue=item_values[column_index])
                if neuerWert:
                    alter_wert = getraenk.menge
                    getraenk.menge = neuerWert
            elif column_index == 3: 
                neuerWert = simpledialog.askstring("Bearbeiten", "Neue Verpackung:", initialvalue=item_values[column_index])
                if neuerWert:
                    alter_wert = getraenk.verpackung
                    getraenk.verpackung = neuerWert
            elif column_index == 4:
                neuerWert = simpledialog.askfloat("Bearbeiten", "Neuer Alkoholgehalt:", initialvalue=item_values[column_index])
                if neuerWert is not None:               # is not None, besser als neuerWert: | wenn wert 0.0 etc, dann ist automatisch false (:
                    #print(f" TRUE Neuer Wert {neuerWert}")
                    alter_wert = getraenk.alkoholgehalt
                    getraenk.alkoholgehalt = float(neuerWert)
                    #print(f"Alkoholgehalt vor dem Speichern: {getraenk.alkoholgehalt}")
                else:
                    #print(f" FALSE NeuerWert: {neuerWert}")
                    print("Alkoholgehalt konnte nicht gesetzt werden.")
            tree.item(selected_item, values=(getraenk.name,
                                              self.getraenkeListe[int(selected_item)].preis,
                                              self.getraenkeListe[int(selected_item)].menge,
                                              self.getraenkeListe[int(selected_item)].verpackung,
                                              self.getraenkeListe[int(selected_item)].alkoholgehalt))

            self.getraenke_speichern()
            print(f"Neue Werte gespeichert für Getränk: {getraenk.name}")

        tree.bind("<Double-1>", on_edit)
        #


    

    def openVending(self):
        VK.Verkaufsfenster(self.root,self.getraenkeListe)