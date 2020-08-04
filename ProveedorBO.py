import mysql.connector

class ProveedorBO:

    def __init__(self):
        #Conexión con la base de datos
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "", 
                                     db ="mydb")

    #destruccion del objeto
    def __del__(self):
        self.db.close() 
    
    #guardar el proveedor en base de datos
    def guardar(self, proveedor):
        try:
            if(self.validar(proveedor)):
                if(not self.exist(proveedor)): 
                    #insertar al proveedor
                    insertSQL = "INSERT INTO proveedor (`PK_idproveedor`, `Nombre`, `Direccion`, `Telefono`, `Correo`) VALUES (%s, %s, %s, %s, %s)"
                    insertValores =  (proveedor.PK_ID_PROV.get(),proveedor.NOMBRE.get(),proveedor.DIRECCION.get(),proveedor.TELEFONO.get(),proveedor.CORREO.get())
                    print(insertValores)
                    cursor = self.db.cursor() 
                    cursor.execute(insertSQL, insertValores) 
                    self.db.commit() 
                else:
                    raise Exception('El ID del proveedor indicada en el formulario existe en la base de datos') 
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
        #eliminar proveedor
    def eliminar(self, proveedor):
        try:
            #eliminar proveedor
            deleteSQL = "delete from proveedor where PK_idproveedor = " + proveedor.PK_ID_PROV.get()
            cursor = self.db.cursor() 
            cursor.execute(deleteSQL)
            self.db.commit() 
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))
    
    #modificar proveedor
    def modificar(self, proveedor):
        try:
            if(self.validar(proveedor)):
                if(self.exist(proveedor)): 
                    #modifivca proveedor
                    updateSQL = "UPDATE proveedor set `Nombre` = %s, `Direccion` = %s, `Telefono` = %s, `Correo` = %s WHERE `PK_idproveedor` =  %s"
                    updateValores = (proveedor.NOMBRE.get(),proveedor.DIRECCION.get(),proveedor.TELEFONO.get(),proveedor.CORREO.get(),proveedor.PK_ID_PROV.get())
                    print(updateValores)
                    cursor = self.db.cursor() 
                    cursor.execute(updateSQL, updateValores) 
                    self.db.commit() 
                else:
                    raise Exception('El ID proveedor indicada en el formulario no existe en la base de datos') 
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información') 
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #si existe o no 
    def exist(self , proveedor):
        try:
            existe = False
            selectSQL = "Select * from proveedor where PK_idproveedor = " + proveedor.PK_ID_PROV.get()
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
            selectSQL = "select PK_idproveedor as idproveedor, \
                            Nombre, Direccion, \
                            Telefono, Correo \
                        from proveedor" 
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

    #consulta al proveedor
    def consultarCliente(self, proveedor):
        try:
            selectSQL = "Select * from proveedor where PK_idproveedor = " + proveedor.PK_ID_PROV.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            clienteDB = cursor.fetchone()
            #Metodo obtiene un solo registro o none si no existe información
            if (clienteDB) : 
                proveedor.PK_ID_PROV.set(clienteDB[0]),
                proveedor.NOMBRE.set(clienteDB[1])
                proveedor.DIRECCION.set(clienteDB[2])
                proveedor.TELEFONO.set(clienteDB[3])
                proveedor.CORREO.set(clienteDB[4])
            else:
                raise Exception("La cédula consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))  

    def validar (self, proveedor):
        valido = True
        proveedor.printInfo()
        if proveedor.PK_ID_PROV.get() == "" :
            valido = False
        
        if proveedor.NOMBRE.get() == "" :
            valido = False

        if proveedor.DIRECCION.get() == "" :
            valido = False

        if proveedor.TELEFONO.get() == "" :
            valido = False

        if proveedor.CORREO.get() == "" :
            valido = False

        return valido