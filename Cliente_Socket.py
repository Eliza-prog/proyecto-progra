#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM #socket
from threading import Thread #hilos
from tkinter import * #tkinter
from tkinter import font #fuentes
from tkinter import messagebox as msg 
from tkinter import ttk
import tkinter #tkinter

class Chat_C: 

    def __init__(self):

        #Pantalla
        self.raiz = Tk()
        self.raiz.title ("Chat")
        self.raiz.geometry('350x480') 

        #Fuente y Variables
        self.fuente = font.Font(weight="bold")
        #mensaje
        self.mns = StringVar() 
        self.mns.set("Digite su mensaje aqui")
        #tiempo
        self.precision = 10
        self.tiempo = 1

        #Titulo
        self.lb_tituloPantalla = Label(self.raiz, text = "CHAT CLIENTE - SERVIDOR", font = self.fuente)
        self.lb_tituloPantalla.place(x = 60, y = 20)

        #Mensajes + Scrollbar
        self.Scr_vertical = Scrollbar(self.raiz)  
        self.lbx_mensajes = Listbox(self.raiz, height=20, width=50, yscrollcommand = self.Scr_vertical.set)  
        self.lbx_mensajes.place(x = 20, y = 70) 

        self.Scr_vertical.config(command = self.lbx_mensajes.yview)
        self.Scr_vertical.pack(side = RIGHT, fill = Y)

        self.txt_mensaje = Entry(self.raiz, textvariable=self.mns, justify="center", width=50)
        self.txt_mensaje.place(x = 20, y = 400)

        #boton enviar
        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command = self.enviar)
        self.bt_enviar.place(x = 110, y = 430)

        #tiempo
        self.lb_tiempo = Label(self.raiz, font=("bold", 20), text="00:00:00")
        self.lb_tiempo.place(x=110, y=20)

        #cerrado
        self.raiz.protocol("WM_DELETE_WINDOW", self.cerrando)

        #variables socket (host, puerto)
        self.HOST = 'localhost' 
        self.PORT = 33000 

        #bytes (para mensajes) / direccion
        self.BYTES = 1024
        self.ADDR = (self.HOST, self.PORT)

        #coneccion del cliente con el servidor
        self.cliente_socket = socket(AF_INET, SOCK_STREAM) #socket del cliente 
        self.cliente_socket.connect(self.ADDR) #se conecta con el host y puerto iniidcado 

        #hilos 
        self.recibir_thread = Thread(target=self.recibir)
        self.recibir_thread.start()

        self.iniciotiempo()
         
        self.raiz.mainloop()

    #mensajes que se reciven de otros usuarios 
    def recibir(self):
        while True:
            try:
                msg = self.cliente_socket.recv(self.BYTES).decode("utf8") #recivir el mensaje 
                self.lbx_mensajes.insert(tkinter.END, msg) #mostrar el mensaje 
            except OSError:  #reporta errores del socket 
                break

    #Enviar los mensajes del usuario            
    def enviar(self, event=None):  
        msg = self.mns.get() #Obtiene el mensaje 
        self.mns.set("") #setea para nuevos mensajes 
        self.cliente_socket.send(bytes(msg, "utf8")) #envia el mensaje 
        if msg == "{salir}": #si el mensajes es de salida se cierra la conexion del usuario 
            self.cliente_socket.close() #se cierra la conexion 
            self.raiz.destroy() #se cierra la ventana del usuario 

    def cerrando(self, event=None):
        self.mns.set("{salir}") #setea el mensaje para que de forma recursiva se cierre
        self.enviar() #llama al metodo enviar 

    def iniciotiempo(self): #reloj
        self.tiempo = self.tiempo + self.precision #tiempo con presicion de 10 
        segundos, milisegundos = divmod(self.tiempo, 1000) #segundo / milisegundos
        minutos, segundos = divmod(segundos, 60) #minutos / segundos

        self.lb_tiempo.config(text="{:02}:{:02}:{:03}".format(minutos, segundos, milisegundos)) #se muestra el tiempo 
        self.lb_tiempo.after(self.precision, self.iniciotiempo) #llamada recursiva 

def main():
    Chat_C()
    return 0

if __name__ == "__main__": 
    main()