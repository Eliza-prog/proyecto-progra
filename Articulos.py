from tkinter import StringVar
from tkinter import IntVar

class Articulo: 

    def __init__(self):
        self.PK_ID_ART = StringVar()
        self.NOMBRE = StringVar()
        self.CANT_EXI = IntVar()
        self.DESCRIPCION = StringVar()
        self.PRECIO_UN = IntVar()

    def limpiar(self):
        self.PK_ID_ART.set("")
        self.NOMBRE.set("")
        self.CANT_EXI.set("")
        self.DESCRIPCION.set("")
        self.PRECIO_UN.set("")

    def printInfo(self):
        print(f"ID_Articulo: {self.PK_ID_ART.get()}")
        print(f"Nombre del articulo: {self.NOMBRE.get()}")
        print(f"Cantidad existente: {self.CANT_EXI.get()}")
        print(f"Descripcion: {self.DESCRIPCION.get()}")
        print(f"Precio unitario: {self.PRECIO_UN.get()}")