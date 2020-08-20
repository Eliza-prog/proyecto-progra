from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk
from tksheet import Sheet

from Elementos import Articulos
from Elementos import ArticuloBO

class Directorio_A: 

    def __init__(self):
        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Articulos")
        self.raiz.geometry('600x520') 

        #Barra menu
        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar) 

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Proveedor", command=self.abrir_P)
        mantmenu.add_command(label="Clientes", command=self.abrir_C)
        mantmenu.add_command(label="Facturas", command=self.abrir_F)
        mantmenu.add_command(label="Conexion", command=self.abrir_R)

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
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15)
        self.bt_borrar.place(x = 70, y = 220)

        #Boton Enviar
        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command = self.enviarInformacion)
        self.bt_enviar.place(x = 190, y = 220)

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
                            headers = ['ID articulo', 'Nombre', 'Cantidad', 'Descripcion', 'Preio Unitario'],
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
                self.articuloBo.guardar(self.articuloBo)
            else:
                self.articuloBo.modificar(self.articulo)
            
            self.cargarTodaInformacion()
            self.insertando = True
            self.articulo.limpiar() 

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar articulo", "La información del articulo ha sido incluida correctamente") 
            else:
                msg.showinfo("Acción: modificar articulo", "La información del articulo ha sido modificada correctamente") 
        except Exception as e: 
            msg.showerror("Error",  str(e))
    
    #eliminar la info
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            idarticulo = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar a "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.articulo.PK_ID_ART.set(idarticulo)
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
            idarticulo = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            self.articulo.PK_ID_ART.set(idarticulo)
            self.articuloBo = ArticuloBO.ArticuloBO()
            self.articuloBo.consultarArticulo(self.articulo) 
            self.insertando = False
            msg.showinfo("Acción: Consultar proveedor", "La información del proveedor ha sido consultada correctamente") 
            
        except Exception as e: 
            msg.showerror("Error",  str(e))

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
    
    def abrir_R(self):
        from mant_RelacionAP import Conexion_AP
        self.raiz.destroy()
        Conexion_AP()

        self.raiz.mainloop()
       

def main():
    Directorio_A()
    return 0

if __name__ == "__main__":
    main()
