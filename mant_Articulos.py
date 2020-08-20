from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk
from tksheet import Sheet

from Elementos import Articulos
from Elementos import ArticuloBO

from reportlab.pdfgen import canvas as reportPDF
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors

import subprocess

class Directorio_A: 

    def __init__(self):
        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Articulos")
        self.raiz.geometry('680x520') 

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
        self.insertando = True

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

        self.bt_reporte = Button(self.raiz, text="Reporte", width=15, command = self.generarPDFListado)
        self.bt_reporte.place(x = 550, y = 340)

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

    def generarPDFListado(self):
        try:
            #Crea un objeto para la creación del PDF
            nombreArchivo = "ListadoArticulos.pdf"
            rep = reportPDF.Canvas(nombreArchivo)

            #Agrega el tipo de fuente Arial
            registerFont(TTFont('Arial','ARIAL.ttf'))
            
        
            #Crea el texto en donde se incluye la información
            textobject = rep.beginText()
            # Coloca el titulo
            textobject.setFont('Arial', 16)
            textobject.setTextOrigin(10, 800)
            textobject.setFillColor(colors.darkorange)
            textobject.textLine(text='LISTA DE ARTICULOS')
            #Escribe el titulo en el reportes
            rep.drawText(textobject)

            #consultar la informacion de la base de datos
            self.articuloBo = ArticuloBO.ArticuloBO() #se crea un objeto de logica de negocio
            informacion = self.articuloBo.consultar()
            #agrega los titulos de la tabla en la información consultada
            titulos = ["ID articulo", "Nombre del articulo", "Descripcion", "Cant.Existente", "Precio Unitario"]
            informacion.insert(0,titulos)
            #crea el objeto tabla  para mostrar la información
            t = Table(informacion)
            #Le coloca el color tanto al borde de la tabla como de las celdas
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                  ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

            #para cambiar el color de las fichas de hace un ciclo según la cantidad de datos
            #que devuelve la base de datos
            data_len = len(informacion)
            for each in range(data_len):
                if each % 2 == 0:
                    bg_color = colors.whitesmoke
                else:
                    bg_color = colors.lightgrey

                if each == 0 : #Le aplica un estilo diferente a la tabla
                    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), colors.orange)]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

            #acomoda la tabla según el espacio requerido
            aW = 840
            aH = 780
            w, h = t.wrap(aW, aH)
            t.drawOn(rep, 10, aH-h)

            #Guarda el archivo
            rep.save()
            #Abre el archivo desde comandos, puede variar en MacOs es open
            #subprocess.Popen("open '%s'" % nombreArchivo, shell=True)
            subprocess.Popen(nombreArchivo, shell=True) #Windows
        except IOError:
            msg.showerror("Error",  "El archivo ya se encuentra abierto")
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
