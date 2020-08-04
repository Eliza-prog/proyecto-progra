from tkinter import IntVar
from tkinter import StringVar

class Articulo_Proveedor:

    def __init__(self):
        self.PK_ID_CON = StringVar()
        self.FK_ID_ART = StringVar()
        self.FK_ID_PROV = StringVar()
        self.NOM_ART = StringVar()
        self.NOM_PROV = StringVar()

    def limpiar(self): 
        self.FK_ID_ART.set("")
        self.FK_ID_PROV.set("")
    
    def printInfo(self):
        print(f"ID_Articulo: {self.FK_ID_ART.get()}")
        print(f"ID_Proveedor: {self.FK_ID_PROV.get()}")