from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk

class Opc:

    def __init__(self):

        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Opciones Administrador")
        self.raiz.geometry('600x200')  

        #Fuente
        self.fuente = font.Font(weight="bold")
        self.user = StringVar()
        self.pasw = StringVar()
   
        #Titulo 
        self.lb_tituloPantalla = Label(self.raiz, text = "OPCIONES DEL ADMINISTRADOR", font = self.fuente)
        self.lb_tituloPantalla.place(x = 180, y = 20)

        #Boton Mantenimientos 
        self.bt_borrar = Button(self.raiz, text="Mantemientos", width=15, command = self.AbrirMant)
        self.bt_borrar.place(x = 250, y = 60)

        #Boton Chat
        self.bt_enviar = Button(self.raiz, text="Chat clientes", width=15)
        self.bt_enviar.place(x = 250, y = 90)

        #Boton Control
        self.bt_enviar = Button(self.raiz, text="Control clientes", width=15)
        self.bt_enviar.place(x = 250, y = 120)

        self.raiz.mainloop()

    def AbrirMant(self):
        from mant_Clientes import Directorio_C
        self.raiz.destroy()
        Directorio_C()

def main():
    Opc()
    return 0

if __name__ == "__main__": 
    main()
