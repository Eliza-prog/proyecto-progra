from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk
from tksheet import Sheet

from tkcalendar import Calendar, DateEntry

from Elementos import Cliente
from Elementos import ClienteBO

class Directorio_C: 

    def __init__(self):

        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Clientes")
        self.raiz.geometry('600x630') 

        #Barra menu
        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Facturas", command=self.abrir_F)
        mantmenu.add_command(label="Articulos", command=self.abrir_A)
        mantmenu.add_command(label="Proveedores", command=self.abrir_p)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #Objecto cliente
        self.fuente = font.Font(weight="bold")
        self.cliente = Cliente.Cliente()
        self.insertando = True

        #Titulo 
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE CLIENTES", font = self.fuente)
        self.lb_tituloPantalla.place(x = 180, y = 20)

        #Formulario 

        #Cedula
        self.lb_cedula = Label(self.raiz, text = "Cedula:")
        self.lb_cedula.place(x = 100, y = 60)
        self.txt_cedula = Entry(self.raiz, textvariable=self.cliente.PK_CEDULA, justify="right")
        self.txt_cedula.place(x = 230, y = 60)

        #Nombre
        self.lb_nombre = Label(self.raiz, text = "Nombre:")
        self.lb_nombre.place(x = 100, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.cliente.NOMBRE_C, justify="right", width=30)
        self.txt_nombre.place(x = 230, y = 90)

        #Apellido 1
        self.lb_apellido1 = Label(self.raiz, text = "Primer apellido:")
        self.lb_apellido1.place(x = 100, y = 120)
        self.txt_apellido1 = Entry(self.raiz, textvariable=self.cliente.APELLIDO_1, justify="right", width=30)
        self.txt_apellido1.place(x = 230, y = 120)

        #Apellido 2
        self.lb_apellido2 = Label(self.raiz, text = "Segundo apellido:")
        self.lb_apellido2.place(x = 100, y = 150)
        self.txt_apellido2 = Entry(self.raiz, textvariable=self.cliente.APELLIDO_2, justify="right", width=30)
        self.txt_apellido2.place(x = 230, y = 150)

        #Fecha nacimiento
        self.lb_fec_nacimiento = Label(self.raiz, text = "Fecha nacimiento:")
        self.lb_fec_nacimiento.place(x = 100, y = 180)
        self.txt_fechaNacimiento = Entry(self.raiz, textvariable=self.cliente.FECHA_NACIMIENTO, justify="right", width=30, state="readonly")
        self.txt_fechaNacimiento.place(x = 230, y = 180)
        self.bt_mostrarCalendario = Button(self.raiz, text="...", width=3, command=self.mostrarDatePicker)
        self.bt_mostrarCalendario.place(x = 510, y = 180)

        #Direccion
        self.lb_direccion = Label(self.raiz, text = "Direccion:")
        self.lb_direccion.place(x = 100, y = 210)
        self.txt_direccion = Entry(self.raiz, textvariable=self.cliente.DIRECCION, justify="right", width=30)
        self.txt_direccion.place(x = 230, y = 210)

        #Observaciones
        self.lb_observaciones = Label(self.raiz, text = "Observaciones:")
        self.lb_observaciones.place(x = 100, y = 240)
        self.txt_observaciones = Entry(self.raiz, textvariable=self.cliente.OBSERVACIONES, justify="right", width=30)
        self.txt_observaciones.place(x = 230, y = 240)

        #Telefono 1
        self.lb_telefono_1 = Label(self.raiz, text = "Telefono Principal:")
        self.lb_telefono_1.place(x = 100, y = 270)
        self.txt_telefono_1 = Entry(self.raiz, textvariable=self.cliente.TELEFONO_1, justify="right", width=30)
        self.txt_telefono_1.place(x = 230, y = 270)

        #Telefono 2
        self.lb_telefono_2 = Label(self.raiz, text = "Telefono segundario:")
        self.lb_telefono_2.place(x = 100, y = 300)
        self.txt_telefono_2 = Entry(self.raiz, textvariable=self.cliente.TELEFONO_2, justify="right", width=30)
        self.txt_telefono_2.place(x = 230, y = 300)

        #Boton Limpiar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.limpiarInformacion)
        self.bt_borrar.place(x = 70, y = 340)

        #Boton Enviar
        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command = self.enviarInformacion)
        self.bt_enviar.place(x = 190, y = 340)

        #Boton Cargar
        self.bt_borrar = Button(self.raiz, text="Cargar", width=15, command = self.cargarInformacion)
        self.bt_borrar.place(x = 310, y = 340)

        #Boton Eliminar 
        self.bt_enviar = Button(self.raiz, text="Eliminar", width=15, command = self.eliminarInformacion)
        self.bt_enviar.place(x = 430, y = 340)

        #label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 190, y = 400)

        #cuadro excel
        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['Cédula', 'Nombre', 'Primer Ape.', 'Segundo Ape.', 'Fec. Nacimiento', 'Direccion', 'Observaciones', 'Telefono 1', 'Telefono 2'],
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

        self.sheet.place(x = 20, y = 440)

        #toda informacion
        self.cargarTodaInformacion()
       
        #cierre de raiz
        self.raiz.mainloop()

    #calendario
    def mostrarDatePicker(self):
        #ventana segundaria
        self.top = Toplevel(self.raiz)
        self.cal = Calendar(self.top, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand1", year=2019, month=6, day=16)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="Seleccionar", command = self.seleccionarFecha).pack()

    #Selecciona la fecha
    def seleccionarFecha(self):
        self.cliente.FECHA_NACIMIENTO.set(self.cal.selection_get())
        self.top.destroy()

    #Limpiar
    def limpiarInformacion(self):
        self.cliente.limpiar()
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente")

    #envia la info
    def enviarInformacion(self):
        try:
            self.clienteBo = ClienteBO.ClienteBO() 
            if(self.insertando == True):
                self.clienteBo.guardar(self.cliente)
            else:
                self.clienteBo.modificar(self.cliente)
            
            self.cargarTodaInformacion()
            self.insertando = True
            self.cliente.limpiar() 

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar cliente", "La información del cliente ha sido incluida correctamente") 
            else:
                msg.showinfo("Acción: modificar cliente", "La información del cliente ha sido modificada correctamente") 
        except Exception as e: 
            msg.showerror("Error",  str(e))
    
    #eliminar la info
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            cedula = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar a "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.cliente.PK_CEDULA.set(cedula)
                self.clienteBo = ClienteBO.ClienteBO() 
                self.clienteBo.eliminar(self.cliente) 
                self.cliente.limpiar()
        except Exception as e: 
            msg.showerror("Error",  str(e)) 
            
        self.cargarTodaInformacion() #refrescar la pagina especialmente para llaves foraneas relacionales 

    #cargar toda la info
    def cargarTodaInformacion(self):
        try:
            self.clienteBo = ClienteBO.ClienteBO() 
            resultado = self.clienteBo.consultar()

            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e))

    #selecionado
    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            cedula = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            self.cliente.PK_CEDULA.set(cedula)
            self.clienteBo = ClienteBO.ClienteBO() 
            self.clienteBo.consultarCliente(self.cliente) 
            self.insertando = False
            msg.showinfo("Acción: Consultar cliente", "La información del cliente ha sido consultada correctamente") 
            
        except Exception as e: 
            msg.showerror("Error",  str(e))

    #abrir  
    def abrir_F(self):
        from mant_Factura import Directorio_F
        self.raiz.destroy()
        Directorio_F()

    def abrir_A(self):
        from mant_Articulos import Directorio_A
        self.raiz.destroy()
        Directorio_A() 
    
    def abrir_p(self):
        from mant_Proveedor import Directorio_P
        self.raiz.destroy()
        Directorio_P()

def main():
    Directorio_C()
    return 0

if __name__ == "__main__": 
    main()

