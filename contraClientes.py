from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk

class Main:

    def __init__(self):

        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Acceso a los Clientes")
        self.raiz.geometry('600x200')  

        #Fuente
        self.fuente = font.Font(weight="bold")
        self.user = StringVar()
        self.pasw = StringVar()
   
        #Titulo 
        self.lb_tituloPantalla = Label(self.raiz, text = "ACCESO DEL LOS CLIENTES", font = self.fuente)
        self.lb_tituloPantalla.place(x = 180, y = 20)

        #User
        self.lb_User = Label(self.raiz, text = "User:")
        self.lb_User.place(x = 100, y = 60)
        self.txt_User = Entry(self.raiz, textvariable=self.user, justify="right", width = 30)
        self.txt_User.place(x = 230, y = 60)

        #Password
        self.lb_Password = Label(self.raiz, text = "Password:")
        self.lb_Password.place(x = 100, y = 90)
        self.txt_Password = Entry(self.raiz, textvariable=self.pasw, justify="right", width = 30)
        self.txt_Password.place(x = 230, y = 90)

        #Boton Limpiar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.Limpiar)
        self.bt_borrar.place(x = 190, y = 130)

        #Boton Acceder
        self.bt_enviar = Button(self.raiz, text="Acceder", width=15, command = self.Acceder)
        self.bt_enviar.place(x = 310, y = 130)

        self.raiz.mainloop()

    def Acceder(self):
        if(self.user.get() == "Cliente" and self.pasw.get() == "p34"):
            from Opc_cliente import Opc
            self.raiz.destroy()
            Opc()
        else:
            msg.showinfo("Error", "La contrasena o ususario es incorrecta") 

    def Limpiar(self):
        self.user.set("")
        self.pasw.set("")

def main():
    Main()
    return 0

if __name__ == "__main__": 
    main()
