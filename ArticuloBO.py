import mysql.connector

class ArticuloBO:

    def __init__(self):
        #Conexión con la base de datos
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "", 
                                     db ="mydb")

    #destruccion del objeto
    def __del__(self):
        self.db.close() 
    
    #guardar el articulo en baso de datos
    def guardar(self, articulo):
        try:
            if(self.validar(articulo)):
                if(not self.exist(articulo)):  
                    #insertar el articulo
                    insertSQL = "INSERT INTO articulo (`PK_idarticulo`, `Nombre`, `Cantidad`, `Descripcion`, `Precio`) VALUES (%s, %s, %s, %s, %s)"
                    insertValores =  (articulo.PK_ID_ART.get(),articulo.NOMBRE.get(),articulo.CANT_EXI.get(),articulo.DESCRIPCION.get(),articulo.PRECIO_UN.get())
                    print(insertValores)
                    cursor = self.db.cursor() 
                    cursor.execute(insertSQL, insertValores) 
                    self.db.commit()
                else:
                    raise Exception('El articulo indicado en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #eliminar articulo
    def eliminar(self, articulo):
        try:
            #eliminar el articulo
            deleteSQL = "delete from articulo where PK_idarticulo = " + articulo.PK_ID_ART.get()
            cursor = self.db.cursor() 
            cursor.execute(deleteSQL) 
            self.db.commit() 
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            if str(e) == "1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`mydb`.`conexion`, CONSTRAINT `FK_CONEXION_ARTICULO` FOREIGN KEY (`FK_idarticulo`) REFERENCES `articulo` (`PK_idarticulo`))":
                raise Exception("Primero elimine los datos relacionados al articulo") 
            else: 
                raise Exception(str(e)) 
        except Exception as e:
            raise Exception(str(e))

    #modificar articulo
    def modificar(self, articulo):
        try:
            if(self.validar(articulo)):
                if(self.exist(articulo)): 
                    #modifivca articulo
                    updateSQL = "UPDATE articulo set `Nombre` = %s, `Cantidad` = %s, `Descripcion` = %s, `Precio` = %s WHERE `PK_idarticulo` =  %s"
                    updateValores =  (articulo.NOMBRE.get(),articulo.CANT_EXI.get(),articulo.DESCRIPCION.get(),articulo.PRECIO_UN.get(),articulo.PK_ID_ART.get())
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
    def exist(self , articulo):
        try:
            existe = False
            selectSQL = "Select * from articulo where PK_idarticulo = " + articulo.PK_ID_ART.get()
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
            selectSQL = "select PK_idarticulo as articulo, \
                            Nombre, Descripcion, Cantidad, \
                            Precio \
                        from articulo" 
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
    def consultarArticulo(self, articulo):
        try:
            selectSQL = "Select * from articulo where PK_idarticulo = " + articulo.PK_ID_ART.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            articuloDB = cursor.fetchone()
            #Metodo obtiene un solo registro o none si no existe información
            if (articuloDB) : 
                articulo.PK_ID_ART.set(articuloDB[0]),
                articulo.NOMBRE.set(articuloDB[1])
                articulo.CANT_EXI.set(articuloDB[2])
                articulo.DESCRIPCION.set(articuloDB[3])
                articulo.PRECIO_UN.set(articuloDB[4])
            else:
                raise Exception("El articulo consultado no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e))  

    def validar (self, articulo):
        valido = True
        articulo.printInfo()
        if articulo.PK_ID_ART.get() == "" :
            valido = False
        
        if articulo.NOMBRE.get() == "" :
            valido = False

        if articulo.CANT_EXI.get() == "" :
            valido = False

        if articulo.DESCRIPCION.get() == "" :
            valido = False

        if articulo.PRECIO_UN.get() == "" :
            valido = False

        return valido
