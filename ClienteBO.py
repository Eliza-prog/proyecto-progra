import mysql.connector

class ClienteBO:

    def __init__(self):
        #Conexión con la base de datos
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "", 
                                     db ="mydb")

    #destruccion del objeto
    def __del__(self):
        self.db.close() 
    
    #guardar el cliente en baso de datos
    def guardar(self, cliente):
        try:
            if(self.validar(cliente)):
                if(not self.exist(cliente)):  
                    #insertar al cliente
                    insertSQL = "INSERT INTO clientes (`PK_cedula`, `Nombre`, `Apellido1`, `Apellido2`, `FechaNacimiento`, `Direccion`, `Observaciones`,`Telefono1`,`Telefono2`, `LastUser`, `LastMove`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
                    insertValores =  (cliente.PK_CEDULA.get(),cliente.NOMBRE_C.get(),cliente.APELLIDO_1.get(),cliente.APELLIDO_2.get(),cliente.FECHA_NACIMIENTO.get(),cliente.DIRECCION.get(),cliente.OBSERVACIONES.get(),cliente.TELEFONO_1.get(),cliente.TELEFONO_2.get(),cliente.LAST_USER)
                    print(insertValores)
                    cursor = self.db.cursor() 
                    cursor.execute(insertSQL, insertValores) 
                    self.db.commit()
                else:
                    raise Exception('La cédula indicada en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #eliminar cliente
    def eliminar(self, cliente):
        try:
            #eliminar al cliente
            deleteSQL = "delete from clientes where PK_cedula = " + cliente.PK_CEDULA.get()
            cursor = self.db.cursor() 
            cursor.execute(deleteSQL) 
            self.db.commit() 
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            if str(e) == "1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`mydb`.`facturacion`, CONSTRAINT `FK_FACTURACION_CLIENTES` FOREIGN KEY (`FK_cedula`) REFERENCES `clientes` (`PK_cedula`))":
                raise Exception("Primero elimine los datos relacionados al cliente") 
            else: 
                raise Exception(str(e)) 
        except Exception as e:
            raise Exception(str(e))
 
    #modificar cliente
    def modificar(self, cliente):
        try:
            if(self.validar(cliente)):
                if(self.exist(cliente)): 
                    #modifivca cliente
                    updateSQL = "UPDATE clientes set `Nombre` = %s, `Apellido1` = %s, `apellido2` = %s, `FechaNacimiento` = %s, `Direccion` = %s, `Observaciones` = %s, `Telefono1` = %s, `Telefono2` = %s, `LastUser` = %s, `LastMove` = CURDATE() WHERE `PK_cedula` =  %s"
                    updateValores =  (cliente.NOMBRE_C.get(),cliente.APELLIDO_1.get(),cliente.APELLIDO_2.get(),cliente.FECHA_NACIMIENTO.get(),cliente.DIRECCION.get(),cliente.OBSERVACIONES.get(),cliente.TELEFONO_1.get(),cliente.TELEFONO_2.get(),cliente.LAST_USER,cliente.PK_CEDULA.get())
                    print(updateValores)
                    cursor = self.db.cursor() 
                    cursor.execute(updateSQL, updateValores) 
                    self.db.commit() 
                else:
                    raise Exception('La cédula indicada en el formulario no existe en la base de datos') 
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información') 
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #si existe o no 
    def exist(self , cliente):
        try:
            existe = False
            selectSQL = "Select * from clientes where PK_cedula = " + cliente.PK_CEDULA.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) :
                existe  = True

            return existe
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #condulta datos
    def consultar(self):
        try:
            selectSQL = "select PK_cedula as cedula, \
                            Nombre, Apellido1, Apellido2, \
                            FechaNacimiento, Direccion, Observaciones,\
                            Telefono1, Telefono2 \
                        from clientes" 
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
    
    #condulta datos
    def consultarPDF(self):
        try:
            selectSQL = "select PK_cedula as cedula, \
                            Nombre, Apellido1, Apellido2, \
                            FechaNacimiento, Direccion,\
                            Telefono1 \
                        from clientes" 
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

    #consulta al cliente
    def consultarCliente(self, cliente):
        try:
            selectSQL = "Select * from clientes where PK_cedula = " + cliente.PK_CEDULA.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            clienteDB = cursor.fetchone()
            #Metodo obtiene un solo registro o none si no existe información
            if (clienteDB) : 
                cliente.PK_CEDULA.set(clienteDB[0]),
                cliente.NOMBRE_C.set(clienteDB[1])
                cliente.APELLIDO_1.set(clienteDB[2])
                cliente.APELLIDO_2.set(clienteDB[3])
                #cliente.FECHA_NACIMIENTO.set(cliente[4])
                cliente.DIRECCION.set(clienteDB[5])
                cliente.OBSERVACIONES.set(clienteDB[6])
                cliente.TELEFONO_1.set(clienteDB[7])
                cliente.TELEFONO_2.set(clienteDB[8])
            else:
                raise Exception("La cédula consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))  

    #valida los datos
    def validar (self, cliente):
        valido = True
        cliente.printInfo()
        if cliente.PK_CEDULA.get() == "" :
            valido = False
        
        if cliente.NOMBRE_C.get() == "" :
            valido = False

        if cliente.APELLIDO_1.get() == "" :
            valido = False

        if cliente.APELLIDO_2.get() == "" :
            valido = False

        if cliente.FECHA_NACIMIENTO.get() == "" :
            valido = False
        
        if cliente.DIRECCION.get() == "" :
            valido = False
        
        if cliente.OBSERVACIONES.get() == "" :
            valido = False
        
        if cliente.TELEFONO_1.get() == "" :
            valido = False

        if cliente.TELEFONO_2.get() == "" :
            valido = False

        return valido