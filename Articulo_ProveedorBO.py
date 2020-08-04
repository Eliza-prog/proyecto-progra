import mysql.connector

class Articulo_ProveedorBO:

    def __init__(self):
        #Conexión con la base de datos
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "annyanneko", 
                                     db ="mydb")

    #destruccion del objeto
    def __del__(self):
        self.db.close() 
    
    #guardar la conexion en baso de datos
    def guardar(self, conexion):
        try:
            if(self.validar(conexion)): #datos necesarios
                if(self.exist_P(conexion)): #existe proveedor
                    if(self.exist_A(conexion)): #existe articulo 
                        #insertar la conexion
                        insertSQL = "INSERT INTO conexion (`FK_idproveedor`, `FK_idarticulo`) VALUES (%s, %s)"
                        insertValores =  (conexion.FK_ID_PROV.get(),conexion.FK_ID_ART.get())
                        print(insertValores)
                        cursor = self.db.cursor() 
                        cursor.execute(insertSQL, insertValores) 
                        self.db.commit()
                    else:
                        raise Exception('El articulo indicado en el formulario existe en la base de datos')
                else: 
                    raise Exception('El Proveedor indicado en el formulario existe en la base de datos')   
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #Existe articulo 
    def exist_A(self, conexion):
        try:
            #por le momento sera falso hsta demostrar lo contrario
            existe = False
            selectSQL = "Select * from articulo where PK_idarticulo = " + conexion.FK_ID_ART.get()
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

    #Existe proveedor
    def exist_P(self, conexion):
        try:
            #por le momento sera falso hsta demostrar lo contrario
            existe = False
            selectSQL = "Select * from proveedor where PK_idproveedor = " + conexion.FK_ID_PROV.get()
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
        
    #si existe o no 
    def exist(self, conexion):
        try:
            existe = False
            selectSQL = "Select * from conexion where PK_idconexion = " + conexion.PK_ID_CON.get()
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

    #eliminar conexion
    def eliminar(self, conexion):
        try:
            #eliminar la conexion
            deleteSQL = "delete from conexion where PK_idconexion = " + conexion.PK_ID_CON.get()
            cursor = self.db.cursor() 
            cursor.execute(deleteSQL) 
            self.db.commit() 
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))

    #modificar conexion
    def modificar(self, conexion):
        try:
            if(self.validar(conexion)): #datos necesarios
                if(self.exist(conexion)):  #ya existia dicha conexion
                    if(self.exist_P(conexion)): #existe proveedor
                        if(self.exist_A(conexion)): #existe articulo
                            updateSQL = "UPDATE conexion set `FK_idproveedor` = %s, `FK_idarticulo` = %s WHERE `PK_idconexion` =  %s"
                            updateValores =  (conexion.FK_ID_PROV.get(),conexion.FK_ID_ART.get(),conexion.PK_ID_CON.get())
                            print(updateValores)
                            cursor = self.db.cursor() 
                            cursor.execute(updateSQL, updateValores) 
                            self.db.commit() 
                            conexion.NOM_PROV.set("")
                            conexion.NOM_ART.set("")
                        else:
                            raise Exception('El articulo indicado en el formulario existe en la base de datos')
                    else: 
                        raise Exception('El Proveedor indicado en el formulario NO existe en la base de datos')   
                else:
                    raise Exception('La conexion indicada en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #condulta datos
    def consultar(self):
        try:
            selectSQL = "select PK_idconexion as conexion, \
                            FK_idproveedor , FK_idarticulo\
                        from conexion" 
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

      #consulta la conexion
    def consultarConexion(self, conexion):
        try:
            selectSQL = "Select * from conexion where PK_idconexion = " + conexion.PK_ID_CON.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            conexionDB = cursor.fetchone()
            #Metodo obtiene un solo registro o none si no existe información
            if (conexionDB) : 
                conexion.PK_ID_CON.set(conexionDB[0]),
                conexion.FK_ID_ART.set(conexionDB[1])
                conexion.FK_ID_PROV.set(conexionDB[2])

                NombrePSQL = "Select Nombre from proveedor where PK_idproveedor = " + conexion.FK_ID_PROV.get() #busca el nombre del proveedor asiociado
                cursor = self.db.cursor()
                cursor.execute(NombrePSQL)
                conexionDB = cursor.fetchone()
                if (conexionDB): 
                    conexion.NOM_PROV.set(conexionDB[0]) #devuelve el nombre 
            
                NombreASQL = "Select Nombre from articulo where PK_idarticulo = " + conexion.FK_ID_ART.get() #busca al nosmbre del ariculo asociado
                cursor = self.db.cursor()
                cursor.execute(NombreASQL)
                conexionDB = cursor.fetchone()
                if (conexionDB): 
                    conexion.NOM_ART.set(conexionDB[0]) #devuelve el nombre 

            else:
                raise Exception("El numero de conexion consultada no existe en la base de datos") 
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))  

    #valida los datos
    def validar (self, articulo_proveedor):
        valido = True
        articulo_proveedor.printInfo()
        if articulo_proveedor.FK_ID_ART.get() == "" :
            valido = False
        
        if articulo_proveedor.FK_ID_PROV.get() == "" :
            valido = False   

        return valido