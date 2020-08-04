from tkinter import StringVar
from tkinter import IntVar

class Factura:

    def __init__(self):
        self.PK_N_FACTURA = StringVar()
        self.FK_CEDULA = StringVar() 
        self.TIEMPO_USO = StringVar()
        self.MONTO = IntVar()
        self.FK_ID_ART = StringVar()
        self.CLIENTE = StringVar()
        self.APELLIDO_1 = StringVar()
        self.APELLIDO_2 = StringVar()
        self.ARTICULO = StringVar()

    def limpiar(self):
        self.PK_N_FACTURA.set("")
        self.FK_CEDULA.set("")
        self.TIEMPO_USO.set("")
        self.MONTO.set("")
        self.FK_ID_ART.set("")     

    def printInfo(self):
        print(f"ID_Factura: {self.PK_N_FACTURA.get()}")
        print(f"Cedula: {self.FK_CEDULA.get()}")
        print(f"Tiempo de uso: {self.TIEMPO_USO.get()}")
        print(f"Monto total: {self.MONTO.get()}")
        print(f"ID_Articulo: {self.FK_ID_ART.get()}")
        
        