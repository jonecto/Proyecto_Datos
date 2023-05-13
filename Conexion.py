import psycopg2
import pandas as pd



try:
    connection = psycopg2.connect(
       host="localhost",
       database="DB_proyecto", #el nombre que se le haya puesto al DB al crearlo en sql
       user="postgres",
       password="" #poner contraseña propia
   )
    print('Conexión exitosa')
    
    cursor = connection.cursor()

#Tabla1

    query_tabla1 = "Select * From tipo_empleo;"
    cursor.execute(query_tabla1)
    tipo_empleo = cursor.fetchall() #Lista de tuplas con la info de la tabla. No están los nombres de las colunas de la tabla tipo_empleo
   
    columnas = [desc[0] for desc in cursor.description]
    #El atributo .description da una lista de tuplas con informacion de la conexión. En las primeras poscición con indice 0 aparecen los nombres de las columnas
    
    tipo_empleoDF = pd.DataFrame(tipo_empleo, columns=columnas) #df de la primera tabla
   
    for tipo_empleo_i in tipo_empleo:
        print(tipo_empleo_i) #Imprime cada tupla de la tabla tipo de empleo
   
#Tabla2
   
    query_tabla2 = "Select * From empresa;"
    cursor.execute(query_tabla2)
    empresa = cursor.fetchall()       
    
    columnas = [desc[0] for desc in cursor.description]
    empresaDF = pd.DataFrame(empresa, columns=columnas)
    
    for empresa_i in empresa:
        print(empresa_i)  

#Tabla3

    query_tabla3 = "Select * From nivel_experiencia;"
    cursor.execute(query_tabla3)
    nivel_experiencia = cursor.fetchall()    
   
    columnas = [desc[0] for desc in cursor.description]
    nivel_experienciaDF = pd.DataFrame(nivel_experiencia, columns=columnas)
   
    for nivel_experiencia_i in nivel_experiencia:
        print(nivel_experiencia_i)

#Tabla4

    query_tabla4 = "Select * From empleado;"
    cursor.execute(query_tabla4)
    empleado = cursor.fetchall()    
    
    columnas = [desc[0] for desc in cursor.description]
    empleadoDF = pd.DataFrame(empleado, columns=columnas)
    
    for empleado_i in empleado:
        print(empleado_i)

#Tabla5 

    query_tabla5 = "Select * From empleo;"
    cursor.execute(query_tabla5)
    empleo = cursor.fetchall()    
    
    columnas = [desc[0] for desc in cursor.description]
    empleoDF = pd.DataFrame(empleo, columns=columnas)
    
    for empleo_i in empleo:
        print(empleo_i)             
     
#Tabla6

    query_tabla6 = "Select * From trabaja;"
    cursor.execute(query_tabla6)
    trabaja = cursor.fetchall()    
    
    columnas = [desc[0] for desc in cursor.description]
    trabajaDF = pd.DataFrame(trabaja, columns=columnas)
    
    for trabaja_i in trabaja:
        print(trabaja_i)
     
   
    
except Exception as ex:
    print(ex)

finally:
    connection.close()
    print("conexion cerrada")