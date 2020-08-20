import mysql.connector

class FacturaBO:

    def __init__(self):
        #Conexión con la base de datos
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "", 
                                     db ="mydb")  
    
    #destruccion del objeto
    def __del__(self):
        self.db.close() 

    #guardar la factura en base de datos
    def guardar(self, factura):
        try:
            #se valida que tenga la información 
            if(self.validar(factura)):

                #mientras no exista    
                if(not self.exist(factura)): 
                    if(self.exist_C(factura)): #existe cliente
                        if(factura.FK_ID_ART.get() == ""): #con articulo
                            #insertar la factura
                            insertSQL = "INSERT INTO facturacion (`NumFactura`, `FK_cedula`, `TiempoUso`, `Monto`, `FK_idarticulo`) VALUES (%s, %s, %s, %s, NULL)"
                            insertValores =  (factura.PK_N_FACTURA.get(),factura.FK_CEDULA.get(),factura.TIEMPO_USO.get(),factura.MONTO.get())
                            print(insertValores)
                            cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                            cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                            self.db.commit() #crea un commit en la base de datos
                        elif(self.exist_A(factura)): #sin articulo
                            #insertar la factura
                            insertSQL = "INSERT INTO facturacion (`NumFactura`, `FK_cedula`, `TiempoUso`, `Monto`, `FK_idarticulo`) VALUES (%s, %s, %s, %s, %s)"
                            insertValores =  (factura.PK_N_FACTURA.get(),factura.FK_CEDULA.get(),factura.TIEMPO_USO.get(),factura.MONTO.get(),factura.FK_ID_ART.get())
                            print(insertValores)
                            cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                            cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                            self.db.commit() #crea un commit en la base de datos
                        else: 
                            raise Exception('El ID articulo indicado en el formulario NO existe en la base de datos')
                    else:
                        raise Exception('La cédula indicada en el formulario NO existe en la base de datos')  # si no existe el registro con la misma cedual genera el error
                else: 
                      raise Exception('La factura indicada en el formulario existe en la base de datos')
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #modificar factura 
    def modificar(self, factura):
        try:
            if(self.exist(factura)): #ya existe la factura
                if(self.validar(factura)): #datos necesarios
                    if(self.exist_C(factura)): #existe el cliente
                        if(factura.FK_ID_ART.get() == "None" or factura.FK_ID_ART.get() == ""): #sin articulo
                            #modifivca fractura 
                            updateSQL = "UPDATE facturacion set `FK_cedula` = %s, `TiempoUso` = %s, `Monto` = %s, `FK_idarticulo` = NULL WHERE `NumFactura` =  %s"
                            updateValores =  (factura.FK_CEDULA.get(),factura.TIEMPO_USO.get(),factura.MONTO.get(),factura.PK_N_FACTURA.get())
                            print(updateValores)
                            cursor = self.db.cursor() 
                            cursor.execute(updateSQL, updateValores) 
                            self.db.commit() 
                            #se setean las varables para nueva informacion
                            factura.CLIENTE.set("")
                            factura.APELLIDO_1.set("")
                            factura.APELLIDO_2.set("")
                            factura.ARTICULO.set("")
                        elif(self.exist_A(factura)): #con articulo
                            #modificar la factura
                            updateSQL = "UPDATE facturacion set `FK_cedula` = %s,`TiempoUso` = %s, `Monto` = %s, `FK_idarticulo` = %s WHERE `NumFactura` =  %s"
                            updateValores =  (factura.FK_CEDULA.get(),factura.TIEMPO_USO.get(),factura.MONTO.get(),factura.FK_ID_ART.get(),factura.PK_N_FACTURA.get())
                            print(updateValores)
                            cursor = self.db.cursor() 
                            cursor.execute(updateSQL, updateValores) 
                            self.db.commit() 
                            #se setean las varables para nueva informacion
                            factura.CLIENTE.set("")
                            factura.APELLIDO_1.set("")
                            factura.APELLIDO_2.set("")
                            factura.ARTICULO.set("")
                    else:
                        raise Exception('La cédula indicada en el formulario no existe en la base de datos') 
                else:
                    raise Exception('Los datos no fueron digitados por favor validar la información') 
            else:
                raise Exception('El numero de factura indicada en el formulario no existe en la base de datos') 
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #si existe o no 
    def exist(self , factura):
        try:
            #por le momento sera falso hsta demostrar lo contrario
            existe = False
            selectSQL = "Select * from facturacion where NumFactura = " + factura.PK_N_FACTURA.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) : #Metodo obtiene un solo registro o none si no existe información
                existe  = True

            return existe
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #existe cliente
    def exist_C(self, factura):
        try:
            #por le momento sera falso hsta demostrar lo contrario
            existe = False
            selectSQL = "Select * from clientes where PK_cedula = " + factura.FK_CEDULA.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) : #Metodo obtiene un solo registro o none si no existe información
                existe  = True

            return existe
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #existe articulo 
    def exist_A(self, factura):
        try:  
            #por le momento sera falso hsta demostrar lo contrario
            existe = False
            selectSQL = "Select * from articulo where PK_idarticulo = " + factura.FK_ID_ART.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) : #Metodo obtiene un solo registro o none si no existe información
                existe  = True
            
            return existe
             
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    
    #eliminar factura
    def eliminar(self, factura):
        try:
                #eliminar la factura
                deleteSQL = "delete from facturacion where NumFactura = " + factura.PK_N_FACTURA.get()
                cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                cursor.execute(deleteSQL) #ejecuta el SQL con las valores
                self.db.commit() #crea un commit en la base de datos
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))
    
     #condulta datos
    def consultar(self):
        try:
            selectSQL = "select NumFactura as factura, \
                            FK_cedula, TiempoUso, Monto, \
                            FK_idarticulo\
                        from facturacion" 
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            myresult = cursor.fetchall()
            final_result = [list(i) for i in myresult]
            return final_result
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))
    
    #consulta al factura
    def consultarFactura(self, factura):
        try:
            selectSQL = "Select * from facturacion where NumFactura = " + factura.PK_N_FACTURA.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            facturaDB = cursor.fetchone()
            #Metodo obtiene un solo registro o none si no existe información
            if (facturaDB) : 
                factura.PK_N_FACTURA.set(facturaDB[0]),
                factura.FK_CEDULA.set(facturaDB[1])
                factura.TIEMPO_USO.set(facturaDB[2])
                factura.MONTO.set(facturaDB[3])
                factura.FK_ID_ART.set(facturaDB[4])

                NombreSQL = "Select Nombre, Apellido1, Apellido2 from clientes where PK_cedula = " + factura.FK_CEDULA.get() #nombre, apellidos del cliente asociado
                cursor = self.db.cursor()
                cursor.execute(NombreSQL)
                facturaDB = cursor.fetchone()
                if (facturaDB): 
                    factura.CLIENTE.set(facturaDB[0]) #se obtiene nombre
                    factura.APELLIDO_1.set(facturaDB[1]) #se obtiene apellido 1 
                    factura.APELLIDO_2.set(facturaDB[2]) #se obtiene apellido 2 
            
                if(not factura.FK_ID_ART.get() == "None"): #si hay articulo
                    NombreSQL = "Select Nombre from articulo where PK_idarticulo = " + factura.FK_ID_ART.get()
                    cursor = self.db.cursor()
                    cursor.execute(NombreSQL)
                    facturaDB = cursor.fetchone()
                    if (facturaDB): 
                        factura.ARTICULO.set(facturaDB[0])
                else:
                    factura.ARTICULO.set("")    

            else:
                raise Exception("El numero de factura consultada no existe en la base de datos") 
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))  

    def validar (self, factura):
        valido = True
        factura.printInfo()
        if factura.PK_N_FACTURA.get() == "" :
            valido = False
        
        if factura.FK_CEDULA.get() == "" :
            valido = False

        if factura.TIEMPO_USO.get() == "" :
            valido = False

        if factura.MONTO.get() == "" :
            valido = False
        
        return valido

   

   
