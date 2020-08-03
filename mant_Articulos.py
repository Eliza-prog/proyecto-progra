from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk

from Elementos import Articulos

class Directorio_A: 

    def __init__(self):
        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Articulos")
        self.raiz.geometry('600x600') 

        #Barra menu
        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Proveedor", command=self.abrir_P)
        mantmenu.add_command(label="Clientes", command=self.abrir_C)
        mantmenu.add_command(label="Facturas", command=self.abrir_F)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #Objecto Articulo
        self.fuente = font.Font(weight="bold")
        self.articulo = Articulos.Articulo()

        #Titulo 
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE ARTICULOS", font = self.fuente)
        self.lb_tituloPantalla.place(x = 180, y = 20)

        #Formulario 

        #ID articulo
        self.lb_cedula = Label(self.raiz, text = "ID articulo:")
        self.lb_cedula.place(x = 100, y = 60)
        self.txt_cedula = Entry(self.raiz, textvariable=self.articulo.PK_ID_ART, justify="right")
        self.txt_cedula.place(x = 230, y = 60)

        #Nombre
        self.lb_nombre = Label(self.raiz, text = "nombre del articulo:")
        self.lb_nombre.place(x = 100, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.articulo.NOMBRE, justify="right", width=30)
        self.txt_nombre.place(x = 230, y = 90)

        #Cantidad existente
        self.lb_apellido1 = Label(self.raiz, text = "Cantidad existente:")
        self.lb_apellido1.place(x = 100, y = 120)
        self.txt_apellido1 = Entry(self.raiz, textvariable=self.articulo.CANT_EXI, justify="right")
        self.txt_apellido1.place(x = 230, y = 120)

        #descripcion
        self.lb_apellido2 = Label(self.raiz, text = "Descripcion:")
        self.lb_apellido2.place(x = 100, y = 150)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.articulo.DESCRIPCION, justify="right", width=30)
        self.txt_apellido2.place(x = 230, y = 150)

        #Precio unitario
        self.lb_apellido1 = Label(self.raiz, text = "Precio unitario:")
        self.lb_apellido1.place(x = 100, y = 180)
        self.txt_apellido1 = Entry(self.raiz, textvariable=self.articulo.PRECIO_UN, justify="right")
        self.txt_apellido1.place(x = 230, y = 180)

        #Boton Limpiar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.limpiarInformacion)
        self.bt_borrar.place(x = 230, y = 210)

        #Boton Enviar
        self.bt_enviar = Button(self.raiz, text="Enviar", width=15)
        self.bt_enviar.place(x = 370, y = 210)

        self.raiz.mainloop()

    #Limpiar
    def limpiarInformacion(self):
        self.articulo.limpiar()
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente")

    #abrir   
    def abrir_P(self):
        from mant_Proveedor import Directorio_P
        self.raiz.destroy()
        Directorio_P()
        
    def abrir_C(self):
        from mant_Clientes import Directorio_C
        self.raiz.destroy()
        Directorio_C()
    
    def abrir_F(self):
        from mant_Factura import Directorio_F
        self.raiz.destroy()
        Directorio_F()

        self.raiz.mainloop()
       

def main():
    Directorio_A()
    return 0

if __name__ == "__main__":
    main()