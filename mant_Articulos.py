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
        mantmenu.add_command(label="Proveedor", command=self.abrir_p)
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
        self.lb_PK_ID_ART = Label(self.raiz, text = "ID articulo:")
        self.lb_PK_ID_ART.place(x = 100, y = 60)
        self.txt_PK_ID_ART = Entry(self.raiz, textvariable=self.articulo.PK_ID_ART, justify="right")
        self.txt_PK_ID_ART.place(x = 230, y = 60)

        #Nombre
        self.lb_NOMBRE = Label(self.raiz, text = "nombre del articulo:")
        self.lb_NOMBRE.place(x = 100, y = 90)
        self.txt_NOMBRE = Entry(self.raiz, textvariable=self.articulo.NOMBRE, justify="right", width=30)
        self.txt_NOMBRE.place(x = 230, y = 90)

        #Cantidad existente
        self.lb_CANT_EXI = Label(self.raiz, text = "Cantidad existente:")
        self.lb_CANT_EXI.place(x = 100, y = 120)
        self.txt_CANT_EXI = Entry(self.raiz, textvariable=self.articulo.CANT_EXI, justify="right")
        self.txt_CANT_EXI.place(x = 230, y = 120)

        #descripcion
        self.lb_DESCRIPCION = Label(self.raiz, text = "Descripcion:")
        self.lb_DESCRIPCION.place(x = 100, y = 150)
        self.txt_DESCRIPCION = Entry(self.raiz, textvariable=self.articulo.DESCRIPCION, justify="right", width=30)
        self.txt_DESCRIPCION.place(x = 230, y = 150)

        #Precio unitario
        self.lb_PRECIO_UN = Label(self.raiz, text = "Precio unitario:")
        self.lb_PRECIO_UN.place(x = 100, y = 180)
        self.txt_PRECIO_UN = Entry(self.raiz, textvariable=self.articulo.PRECIO_UN, justify="right")
        self.txt_PRECIO_UN.place(x = 230, y = 180)

        #Boton Limpiar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.limpiarInformacion)
        self.bt_borrar.place(x = 230, y = 210)

        #Boton Enviar
        self.bt_enviar = Button(self.raiz, text="Enviar", width=15)
        self.bt_enviar.place(x = 370, y = 210)

        #Boton Cargar
        self.bt_borrar = Button(self.raiz, text="Cargar", width=15, command = self.cargarInformacion) 
        self.bt_borrar.place(x = 310, y = 220)

        #Boton Eliminar 
        self.bt_enviar = Button(self.raiz, text="Eliminar", width=15, command = self.eliminarInformacion)
        self.bt_enviar.place(x = 430, y = 220)

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 190, y = 275)

        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['PK_ID_ART', 'Nombre', 'CANT_EXI', 'DESCRIPCION', 'PRECIO_UN'],
                            height = 170,
                            width = 560
                            ) 

        #hoja excel 
        self.sheet.enable_bindings(("single_select",
                                         "column_select",
                                         "row_select",
                                         "column_width_resize",
                                         "double_click_column_resize",
                                         "arrowkeys",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
                                         "rc_select",
                                         "rc_insert_column",
                                         "rc_delete_column",
                                         "rc_insert_row",
                                         "rc_delete_row"))

        self.sheet.place(x = 20, y = 310)

        #toda informacion
        self.cargarTodaInformacion()

        #cierre raiz
        self.raiz.mainloop()
    
    #Limpiar
    def limpiarInformacion(self):
        self.articulo.limpiar()
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente")

    #envia la info
    def enviarInformacion(self):
        try:
            self.articuloBo = ArticuloBO.ArticuloBO() 
            if(self.insertando == True):
                self.articuloBo.guardar(self.articulo)
            else:
                self.articuloBo.modificar(self.articulo)
            
            self.cargarTodaInformacion()
            self.insertando = True
            self.articulo.limpiar() 

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar proveedor", "La información del proveedor ha sido incluida correctamente") 
            else:
                msg.showinfo("Acción: modificar proveedor", "La información del proveedor ha sido modificada correctamente") 
        except Exception as e: 
            msg.showerror("Error",  str(e))
    
    #eliminar la info
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            ID_ART = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            NOMBRE = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar a "+NOMBRE+" de la base de datos?")
            if resultado == "yes":
                self.articulo.PK_ID_ART.set(ID_ART)
                self.articuloBo = ArticuloBO.ArticuloBO() 
                self.articuloBo.eliminar(self.articulo) 
                self.cargarTodaInformacion()
                self.articulo.limpiar()
        except Exception as e: 
            msg.showerror("Error",  str(e))   

    #cargar toda la info
    def cargarTodaInformacion(self):
        try:
            self.articuloBo = ArticuloBO.ArticuloBO() 
            resultado = self.articuloBo.consultar()
            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e))

    #selecionado
    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            ID_ART = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            self.articulo.PK_ID_ART.set(ID_ART)
            self.articuloBo = ArticuloBO.ArticuloBO() 
            self.articuloBo.consultarCliente(self.articulo) 
            self.insertando = False
            msg.showinfo("Acción: Consultar proveedor", "La información del proveedor ha sido consultada correctamente") 
            
        except Exception as e: 
            msg.showerror("Error",  str(e))

    #abrir    
    def abrir_p(self):
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