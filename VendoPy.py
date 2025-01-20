# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, simpledialog
import sv_ttk
from PIL import Image, ImageTk
import os
from Getraenk import Getraenk
import Automat
import Verkaufsfenster as VK






if __name__ == "__main__":
	root = tk.Tk()
	sv_ttk.set_theme("dark")  # sv_ttk theme in "light" "dark"
	
	app = Automat.Automat(root)
	root.mainloop()
	

