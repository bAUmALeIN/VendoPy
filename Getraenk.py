class Getraenk():
	def __init__(self, name, preis, menge, verpackung, alkoholgehalt):
		self.name = name
		self.preis = float(preis)
		self.menge = float(menge)
		self.verpackung = verpackung
		self.alkoholgehalt = float(alkoholgehalt)

	def __repr__(self):
		return (f"Getraenk (Name: {self.name} | Preis: {self.preis} | "
				f"Menge: {self.menge} | Verpackung: {self.verpackung} | "
				f"Alkoholgehalt: {self.alkoholgehalt})")







