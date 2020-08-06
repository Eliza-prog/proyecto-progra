#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM #socket 
from threading import Thread #hilos

#acepta coneciones 
def acep_conexiones():
    while True: #conexion permanente 
        client, client_address = SERVER.accept() #cliente y direccion 
        print("%s:%s se ha conectado." % client_address) 
        client.send(bytes("¡Buenas, digite su nombre y presione ENVIAR!", "utf8")) #envia primer mensaje al cliente
        direcciones[client] = client_address #guarda la direccion 
        Thread(target=cliente_en_llamada, args=(client,)).start() #hilos para ejecutar otros eventos o metodos 


def cliente_en_llamada(client):  # Cliente como argulento / para un solo cliente en especifico 
    nombre = client.recv(BYTES).decode("utf8") #lo que reciva sera el nombre que indentifique al usuario en el chat 
    bienvenida = '¡Bienvenido %s! Si desea salir digite {salir}.' % nombre #mensaje de bienvenida y aviso de salida 
    client.send(bytes(bienvenida, "utf8")) #envia el mensaje al cliente en especifico 
    msg = "¡%s se ha unido al chat!" % nombre #aviso a los demas 
    envio_masa(bytes(msg, "utf8")) #envio de mensaje a los demas 
    clientes[client] = nombre #almacena los usuarios 

    while True: #conexion permanente con cliente especifico
        msg = client.recv(BYTES) #recive mensaje de cliente 
        if msg != bytes("{salir}", "utf8"): #si no es {salir} envia el mensaje a los demas 
            envio_masa(msg, nombre+": ") #envia mensaje 
        else: # de los contrario 
            client.send(bytes("{salir}", "utf8")) #mensaje al cliente: {salir}
            client.close() #cierra la conexion con ese usuario o cliente 
            del clientes[client] #de la lista clientes 
            envio_masa(bytes("%s ha dejado en chat." % nombre, "utf8")) #les avisa que el usuario o cliente dejo el chat
            break


def envio_masa(msg, prefix=""):  # El prefijo es para la identificación del nombre
    for sock in clientes: #para los clientes dentro del arreglo clientes 
        sock.send(bytes(prefix, "utf8")+msg) #mandarles el mensaje 

        
clientes = {} #arreglo clientes 
direcciones = {} #arreglo direcciones (conexion)

HOST = 'localhost' #host
PORT = 33000 #puerto
BYTES = 1024 #bytes (para mensajes)
ADDR = (HOST, PORT) #direccion (host, puerto)

SERVER = socket(AF_INET, SOCK_STREAM) #socket del servidor 
SERVER.bind(ADDR) # enlace con la direccion 

if __name__ == "__main__":
    SERVER.listen(5) #espacio para 5 usuarios 
    print("Esperando conexiones...")
    HILO_ACEPTAR = Thread(target=acep_conexiones) #hilo para aceptar conexiones diferentes 
    HILO_ACEPTAR.start() #empieza el hilo 
    HILO_ACEPTAR.join() #juntar hilos 
    SERVER.close() #cierre del servidor