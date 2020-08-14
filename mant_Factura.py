from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk
from tksheet import Sheet

from Elementos import Factura
from Elementos import FacturaBO

#include para reportes, para instalar reportlab -> pip3 install reportlab
from reportlab.pdfgen import canvas as reportPDF
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors

#Importa para ejecutar un comando
import subprocess

class Directorio_F: 

    def __init__(self):
        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Factura")
        self.raiz.geometry('600x730') 

        #Barra menu
        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Clientes", command=self.abrir_C)
        mantmenu.add_command(label="Articulos", command=self.abrir_A)
        mantmenu.add_command(label="Proveedores", command=self.abrir_p)
        mantmenu.add_command(label="Conexion", command=self.abrir_R)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #Objeto Factura
        self.fuente = font.Font(weight="bold")
        self.factura = Factura.Factura()
        self.insertando = True

        #Titulo
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE FACTURA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 190, y = 20)

        #Formulario 

        #ID factura
        self.lb_cedula = Label(self.raiz, text = "ID factura:")
        self.lb_cedula.place(x = 150, y = 60)
        self.txt_cedula = Entry(self.raiz, textvariable=self.factura.PK_N_FACTURA, justify="right")
        self.txt_cedula.place(x = 300, y = 60)

        #Cedula
        self.lb_nombre = Label(self.raiz, text = "Cedula:")
        self.lb_nombre.place(x = 150, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.factura.FK_CEDULA, justify="right")
        self.txt_nombre.place(x = 300, y = 90)

        #Tiempo
        self.lb_apellido2 = Label(self.raiz, text = "Tiempo utilizado")
        self.lb_apellido2.place(x = 150, y = 120)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.factura.TIEMPO_USO, justify="right", width=30)
        self.txt_apellido2.place(x = 300, y = 120)

        #Monto
        self.lb_apellido2 = Label(self.raiz, text = "Monto Total:")
        self.lb_apellido2.place(x = 150, y = 150)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.factura.MONTO, justify="right", width=30)
        self.txt_apellido2.place(x = 300, y = 150)

        #Articulos asociados
        self.lb_apellido2 = Label(self.raiz, text = "ID Articulo asociado:")
        self.lb_apellido2.place(x = 150, y = 180)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.factura.FK_ID_ART, justify="right")
        self.txt_apellido2.place(x = 300, y = 180)

        #Asociado

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN ASOCIADA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 200, y = 270)

        #Nombre-cedula
        self.lb_apellido2 = Label(self.raiz, text = "Nombre asociado:")
        self.lb_apellido2.place(x = 150, y = 310)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.factura.CLIENTE, justify="right", state = "readonly", width=30)
        self.txt_apellido2.place(x = 300, y = 310)

        #Primer Apellido-cedula
        self.lb_apellido2 = Label(self.raiz, text = "1.ª Apellido asociado:")
        self.lb_apellido2.place(x = 150, y = 340)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.factura.APELLIDO_1, justify="right", state = "readonly", width=30)
        self.txt_apellido2.place(x = 300, y = 340)
    
        #Segundo Apellido-cedula
        self.lb_apellido2 = Label(self.raiz, text = "2.ª Apellido asociado:")
        self.lb_apellido2.place(x = 150, y = 370)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.factura.APELLIDO_2, justify="right", state = "readonly", width=30)
        self.txt_apellido2.place(x = 300, y = 370)

        #Nombre-articulo
        self.lb_apellido2 = Label(self.raiz, text = "Nombre Articulo:")
        self.lb_apellido2.place(x = 150, y = 400)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.factura.ARTICULO, justify="right", state = "readonly", width=30)
        self.txt_apellido2.place(x = 300, y = 400)

        #Botones

        #Boton Limpiar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.limpiarInformacion)
        self.bt_borrar.place(x = 190, y = 220) 

        #Boton Enviar
        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command = self.enviarInformacion)
        self.bt_enviar.place(x = 310, y = 220)

        #Boton Cargar
        self.bt_borrar = Button(self.raiz, text="Cargar", width=15, command = self.cargarInformacion)
        self.bt_borrar.place(x = 430, y = 220)

        #Boton Eliminar 
        self.bt_enviar = Button(self.raiz, text="Eliminar", width=15, command = self.eliminarInformacion)
        self.bt_enviar.place(x = 550, y = 220)

        self.bt_reporte = Button(self.raiz, text="Reporte", width=15, command = self.generarPDFListado)
        self.bt_reporte.place(x = 670, y = 220)

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 200, y = 440)

        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['Factura', 'Cedula', 'Tiempo uso', 'Monto', 'ID articulo'],
                            height = 170,
                            width = 560
                            ) 

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

        self.sheet.place(x = 20, y = 480)

        self.cargarTodaInformacion()

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
            textobject.textLine(text='LISTA DE FACTURA')
            #Escribe el titulo en el reportes
            rep.drawText(textobject)

            #consultar la informacion de la base de datos
            self.facturaBo = FacturaBO.FacturaBO() #se crea un objeto de logica de negocio
            informacion = self.facturaBo.consultar()
            #agrega los titulos de la tabla en la información consultada
            titulos = ["Factura", "Cedula", "Tiempo uso", "Monto", "ID articulo"]
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
        self.factura.limpiar()
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente")
    
    #envia la info
    def enviarInformacion(self):
        try:
            self.facturaBo = FacturaBO.FacturaBO() #se crea un objeto de logica de negocio
            if(self.insertando == True):
                self.facturaBo.guardar(self.factura)
            else:
                self.facturaBo.modificar(self.factura)
            
            self.cargarTodaInformacion()
            self.insertando = True
            self.factura.limpiar() #se limpia el formulario

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar factura", "La información de la factura ha sido incluida correctamente") # Se muestra el mensaje de que todo esta correcto
            else:
                msg.showinfo("Acción: Modificar factura", "La información de la factura ha sido modificada correctamente") # Se muestra el mensaje de que todo esta correcto
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #eliminar la info
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            factura = (self.sheet.get_cell_data(datoSeleccionado[0],0))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar a "+factura+" de la base de datos?")
            if resultado == "yes":
                self.factura.PK_N_FACTURA.set(factura)
                self.facturaBo = FacturaBO.FacturaBO() 
                self.facturaBo.eliminar(self.factura) 
                self.cargarTodaInformacion()
                self.factura.limpiar()
        except Exception as e: 
            msg.showerror("Error",  str(e)) 
    
    #cargar toda la info
    def cargarTodaInformacion(self):
        try:
            self.facturaBo = FacturaBO.FacturaBO() 
            resultado = self.facturaBo.consultar()

            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e))
    
    #selecionado
    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            numero = (self.sheet.get_cell_data(datoSeleccionado[0],0))

            self.factura.PK_N_FACTURA.set(numero)
            self.facturaBo = FacturaBO.FacturaBO() 
            self.facturaBo.consultarFactura(self.factura) 
            self.insertando = False
            msg.showinfo("Acción: Consultar factura", "La información de la factura ha sido consultada correctamente") 
            
        except Exception as e: 
            msg.showerror("Error",  str(e))

    #abrir 
    def abrir_C(self):
        from mant_Cliente import Directorio_C
        self.raiz.destroy()
        Directorio_C()

    def abrir_A(self):
        from mant_Articulos import Directorio_A
        self.raiz.destroy()
        Directorio_A()
     
    def abrir_p(self):
        from mant_Proveedor import Directorio_P
        self.raiz.destroy()
        Directorio_P()

    def abrir_R(self):
        from mant_RelacionAP import Conexion_AP
        self.raiz.destroy()
        Conexion_AP()
       

def main():
    Directorio_F()
    return 0

if __name__ == "__main__":
    main()
