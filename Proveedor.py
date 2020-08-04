from tkinter import StringVar
from tkinter import IntVar

class Proveedor: 

    def __init__(self):
        self.PK_ID_PROV = StringVar()
        self.NOMBRE = StringVar()
        self.DIRECCION = StringVar()
        self.TELEFONO = StringVar()
        self.CORREO = StringVar()

    def limpiar(self): 
        self.PK_ID_PROV.set("")
        self.NOMBRE.set("")
        self.DIRECCION.set("")
        self.TELEFONO.set("")
        self.CORREO.set("")

    def printInfo(self):
        print(f"ID_Proveedor: {self.PK_ID_PROV.get()}")
        print(f"Nombre: {self.NOMBRE.get()}")
        print(f"Direccion: {self.DIRECCION.get()}")
        print(f"Telefono: {self.TELEFONO.get()}")
        print(f"Correo: {self.CORREO.get()}")