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
     
 #ESCENARIO 1
    cursor.execute("select  rank() over (order by avg(salario_usd) desc), empresa.id, pais, tamanio,round(avg(salario_usd),3) from (empresa inner join trabaja on empresa.id = trabaja.id_empresa) inner join empleo on empleo.id = trabaja.id_empleo group by empresa.id;")
    rows = cursor.fetchall()
    graf1 = px.histogram(rows, x = 4, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por empresa")
    
    cursor.execute('''select  rank() over (order by avg(salario_usd) desc), pais,round(avg(salario_usd),3)
	from (empresa inner join trabaja on empresa.id = trabaja.id_empresa)
	inner join empleo on empleo.id = trabaja.id_empleo
	group by pais;''')
    rows = cursor.fetchall()
    graf2 = px.histogram(rows, x = 1,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por país")
    
    cursor.execute('''select  rank() over (order by avg(salario_usd) desc), tamanio,round(avg(salario_usd),3)
	from (empresa inner join trabaja on empresa.id = trabaja.id_empresa)
		inner join empleo on empleo.id = trabaja.id_empleo
	group by tamanio;''')
    rows = cursor.fetchall()
    graf3 = px.histogram(rows, x = 1,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por tipo de empresa")
    
    #ESCENARIO 2
    cursor.execute('''select nivel_experiencia, sum(salario_usd),count(*) 
	from ((empresa inner join trabaja on empresa.id = trabaja.id_empresa)
		inner join empleo on empleo.id = trabaja.id_empleo)
		inner join empleado on empleado.id = trabaja.id_empleado
	group by nivel_experiencia;''')
    rows = cursor.fetchall()
    graf4 = px.histogram(rows, x = 0,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Numero de empleos por nivel de experiencia")
    graf5 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por nivel de experiencia")

    
    app.layout = html.Div(children = [
        html.H1(children = 'Gráfico Edición Cantidad'),
        html.H3(children = 'ESCENARIO 1'),
        html.Div(children = '''
            Determinar de que forma el lugar en donde se situa una empresa y su tamaño clasifica los salarios obtenidos por sus trabajadores,
            destacando en cuales países y tipos de compañias se presentan ofertas mejor remuneradas para los trabajadores.
        '''),
        dcc.Graph(
            id = 'g1',
            figure = graf1
        ),
        dcc.Graph(
            id = 'g2',
            figure = graf2
        ),
        dcc.Graph(
            id = 'g3',
            figure = graf3
        ),
        
        #Escenario 2 codigo
        
        html.H3(children = 'ESCENARIO 2'),
        html.Div(children = '''
            Analizar según los datos en que nivel de experiencia hay más trabajadores y en empleados de que nivel de experiencias las empresas suelen invertir más,
            para de esta forma poder concluir según oportunidades de empleo y expectativas salariales, cual es el mejor grado de experticia a adquirir, teniendo en cuenta
            que avanzar en conocimientos siempre implica un esfuerzo e inversión para un científico de datos.
        '''),
        dcc.Graph(
            id = 'g4',
            figure = graf4
        ),
        dcc.Graph(
            id = 'g5',
            figure = graf5
        ),
        
       
    ],
 )
    
except Exception as ex:
    print(ex)

finally:
    connection.close()
    print("conexion cerrada")
