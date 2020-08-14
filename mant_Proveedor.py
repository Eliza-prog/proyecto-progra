from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk
from tksheet import Sheet

from Elementos import Proveedor
from Elementos import ProveedorBO

#include para reportes, para instalar reportlab -> pip3 install reportlab
from reportlab.pdfgen import canvas as reportPDF
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors

#Importa para ejecutar un comando
import subprocess

class Directorio_P: 

    def __init__(self):
        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Proveedores")
        self.raiz.geometry('600x500') 

        #Barra menu
        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Articulos", command=self.abrir_A)
        mantmenu.add_command(label="Clientes", command=self.abrir_C)
        mantmenu.add_command(label="Facturas", command=self.abrir_F)
        mantmenu.add_command(label="Conexion", command=self.abrir_R)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #Objecto proveedor
        self.fuente = font.Font(weight="bold")
        self.proveedor = Proveedor.Proveedor()
        self.insertando = True

        #Titulo 
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE PROVEEDOR", font = self.fuente)
        self.lb_tituloPantalla.place(x = 180, y = 20)

        #Formulario 

        #ID proveedor
        self.lb_cedula = Label(self.raiz, text = "ID proveedor:")
        self.lb_cedula.place(x = 100, y = 60)
        self.txt_cedula = Entry(self.raiz, textvariable=self.proveedor.PK_ID_PROV, justify="right")
        self.txt_cedula.place(x = 230, y = 60)

        #Nombre
        self.lb_nombre = Label(self.raiz, text = "Nombre completo:")
        self.lb_nombre.place(x = 100, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.proveedor.NOMBRE, justify="right", width=30)
        self.txt_nombre.place(x = 230, y = 90)
        
        #Direccion
        self.lb_observaciones = Label(self.raiz, text = "Direccion:")
        self.lb_observaciones.place(x = 100, y = 120)
        self.txt_observaciones = Entry(self.raiz, textvariable=self.proveedor.DIRECCION, justify="right", width=30)
        self.txt_observaciones.place(x = 230, y = 120)

        #Telefono 1
        self.lb_observaciones = Label(self.raiz, text = "Telefono Principal:")
        self.lb_observaciones.place(x = 100, y = 150)
        self.txt_observaciones = Entry(self.raiz, textvariable=self.proveedor.TELEFONO, justify="right", width=30)
        self.txt_observaciones.place(x = 230, y = 150)

        #Correo
        self.lb_observaciones = Label(self.raiz, text = "Correo electronico:")
        self.lb_observaciones.place(x = 100, y = 180)
        self.txt_observaciones = Entry(self.raiz, textvariable=self.proveedor.CORREO, justify="right", width=30)
        self.txt_observaciones.place(x = 230, y = 180)

        #Boton Limpiar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.limpiarInformacion)
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
        self.bt_reporte.place(x = 550, y = 220)

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 190, y = 275)

        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['ID proveedor', 'Nombre', 'Direccion', 'Telefono', 'Correo'],
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
    
    def generarPDFListado(self):
        try:
            #Crea un objeto para la creación del PDF
            nombreArchivo = "ListadoPersonas.pdf"
            rep = reportPDF.Canvas(nombreArchivo)

            #Agrega el tipo de fuente Arial
            registerFont(TTFont('Arial','ARIAL.ttf'))
            
        
            #Crea el texto en donde se incluye la información
            textobject = rep.beginText()
            # Coloca el titulo
            textobject.setFont('Arial', 16)
            textobject.setTextOrigin(10, 800)
            textobject.setFillColor(colors.darkorange)
            textobject.textLine(text='LISTA DE PROVEEDOR')
            #Escribe el titulo en el reportes
            rep.drawText(textobject)

            #consultar la informacion de la base de datos
            self.proveedorBo = ProveedorBO.ProveedorBO() #se crea un objeto de logica de negocio
            informacion = self.proveedorBo.consultar()
            #agrega los titulos de la tabla en la información consultada
            titulos = ["ID proveedor", "Nombre", "Direccion", "Telefono", "Correo"]
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
            subprocess.Popen("open '%s'" % nombreArchivo, shell=True)
            #subprocess.Popen(nombreArchivo, shell=True) #Windows
        except IOError:
            msg.showerror("Error",  "El archivo ya se encuentra abierto")

    #Limpiar
    def limpiarInformacion(self):
        self.proveedor.limpiar()
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente")

    #envia la info
    def enviarInformacion(self):
        try:
            self.proveedorBo = ProveedorBO.ProveedorBO() 
            if(self.insertando == True):
                self.proveedorBo.guardar(self.proveedor)
            else:
                self.proveedorBo.modificar(self.proveedor)
            
            self.cargarTodaInformacion()
            self.insertando = True
            self.proveedor.limpiar() 

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
            idproveedor = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar a "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.proveedor.PK_ID_PROV.set(idproveedor)
                self.proveedorBo = ProveedorBO.ProveedorBO() 
                self.proveedorBo.eliminar(self.proveedor) 
                self.cargarTodaInformacion()
                self.proveedor.limpiar()
        except Exception as e: 
            msg.showerror("Error",  str(e))   

    #cargar toda la info
    def cargarTodaInformacion(self):
        try:
            self.proveedorBo = ProveedorBO.ProveedorBO() 
            resultado = self.proveedorBo.consultar()

            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e))

    #selecionado
    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            idproveedor = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            self.proveedor.PK_ID_PROV.set(idproveedor)
            self.proveedorBo = ProveedorBO.ProveedorBO() 
            self.proveedorBo.consultarCliente(self.proveedor) 
            self.insertando = False
            msg.showinfo("Acción: Consultar proveedor", "La información del proveedor ha sido consultada correctamente") 
            
        except Exception as e: 
            msg.showerror("Error",  str(e))

    #abrir    
    def abrir_A(self):
        from mant_Articulos import Directorio_A
        self.raiz.destroy()
        Directorio_A()
        
    def abrir_C(self):
        from mant_Cliente import Directorio_C
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
    Directorio_P()
    return 0

if __name__ == "__main__":
    main()
