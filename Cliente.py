from tkinter import StringVar

class Cliente:

    def __init__ (self):
        self.PK_CEDULA = StringVar()
        self.NOMBRE_C = StringVar()
        self.APELLIDO_1 = StringVar()
        self.APELLIDO_2 = StringVar()
        self.FECHA_NACIMIENTO = StringVar()
        self.DIRECCION = StringVar()
        self.OBSERVACIONES = StringVar()
        self.TELEFONO_1 =  StringVar()
        self.TELEFONO_2 = StringVar()
        self.LAST_USER = ""
        self.LAST_MODF = StringVar()

    def limpiar(self):
        self.PK_CEDULA.set("")
        self.NOMBRE_C.set("")
        self.APELLIDO_1.set("")
        self.APELLIDO_2.set("")
        self.FECHA_NACIMIENTO.set("")
        self.DIRECCION.set("")
        self.OBSERVACIONES.set("")
        self.TELEFONO_1.set("")
        self.TELEFONO_2.set("")

    def printInfo(self):
        print(f"Cedula: {self.PK_CEDULA.get()}")
        print(f"Nombre: {self.NOMBRE_C.get()}")
        print(f"Primer Apellido: {self.APELLIDO_1.get()}")
        print(f"Segundo Apellido: {self.APELLIDO_2.get()}")
        print(f"Fecha Nacimiento: {self.FECHA_NACIMIENTO.get()}")
        print(f"Direccion: {self.DIRECCION.get()}")
        print(f"Observaciones: {self.OBSERVACIONES.get()}")
        print(f"Telefono 1: {self.TELEFONO_1.get()}")
        print(f"Telefono 2: {self.TELEFONO_2.get()}")
    