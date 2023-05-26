from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import psycopg2

try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'aja'
    )
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select promocion_remoto, count(*), round(avg(salario_usd),2) from empleo group by promocion_remoto")
    rows = cursor.fetchall()
    app = Dash(__name__)
    fig = px.bar(rows, x = 0, y = 1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "productos por editorial")
   
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

    #ESCENARIO 3
    cursor.execute('''select rank() over(order by round(avg(salario_usd),2) desc), nombre_trabajo, tipo_empleo, round(avg(salario_usd),2) 
    from empleo inner join trabaja on empleo.id=trabaja.id_empleo
    where nivel_experiencia='EN'
    group by cube(nombre_trabajo, tipo_empleo);''')
    rows = cursor.fetchall()
    graf6 = px.histogram(rows, x = 1,y = 3 , pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Salario promedio por título de trabajo para junior")
    graf7 = px.histogram(rows, x = 2,y = 3, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Cantidad de empleos por tipo en capacitación junior")

    #ESCENARIO 4
    cursor.execute('''select promocion_remoto, count(*), round(avg(salario_usd),2)
    from empleo
    group by promocion_remoto;''')
    rows = cursor.fetchall()
    graf8=fig = px.pie(rows, values=2, names=0, title='Population of European continent')
    graf9 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Cantidad de empleos por modalidad en nivel de entrada")

    #ESCENARIO 5
    cursor.execute('''SELECT nombre_trabajo, round(count(*),1) AS cantidad_empleos
    FROM empleo
    GROUP BY nombre_trabajo
    ORDER BY cantidad_empleos DESC
    LIMIT 5;''')
    rows = cursor.fetchall()
    graf10 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "top 5 empleos mas demandados.")
    
    #ESCENARIO 6
    cursor.execute('''select nivel_experiencia, anio,
        round(avg(salario_usd), 1) salario_promedio 
        from empleo
        group by nivel_experiencia, anio
        order by nivel_experiencia;''')
    rows = cursor.fetchall()
    graf11 = px.line(rows, x = 0,y=2, color=1)
    
    cursor.execute('''select tipo_empleo,
       round(avg(CASE WHEN nivel_experiencia = 'SE' THEN salario_usd END), 1) AS Salario_senior, 
       round(avg(CASE WHEN nivel_experiencia = 'MI' THEN salario_usd END), 1) AS Salario_mid,
	   round(avg(CASE WHEN nivel_experiencia = 'EN' THEN salario_usd END), 1) AS Salario_junior,
	   round(avg(CASE WHEN nivel_experiencia = 'EX' THEN salario_usd END), 1) AS salario_ejecutivo
        from empleo
        group by tipo_empleo;''')
    rows = cursor.fetchall()
    print(rows)
    graf12 = px.bar(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por tipo de empleo para Senior")
    graf13 = px.bar(rows, x = 0,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por tipo de empleo para Mid")
    graf14 = px.bar(rows, x = 0,y=3, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por tipo de empleo para junior")
    graf15 = px.bar(rows, x = 0,y=4, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por tipo de empleo para executive")


    app.layout = html.Div(children = [
        html.H1(children = 'ANALISIS SALARIAL DE CIENTIFICOS DE DATOS PERIODO 2020-2023'),
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
        #Primer bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
                     Nicolás: \n
        '''),html.Div(children = '''
                     Sofía: \n
        '''),html.Div(children = '''
                     Victor: \n
        '''),
        ]),
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
        #Segundo bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
                     Nicolás: \n
        '''),html.Div(children = '''
                     Sofía: \n
        '''),html.Div(children = '''
                     Victor: \n
        '''),
        ]),
    #Escenario 3 codigo
        
        html.H3(children = 'ESCENARIO 3'),
        html.Div(children = '''
           Identificar si existe una relación entre el nivel de experiencia, el nombre del empleo 
           y los tipos de empleo obtenidos por los encuestados, enfocandose en los grupos que tienen menos 
           experiencia, para darse una idea del panorama laboral de un recien egresado y cuales son los 
           escenarios más favorables de entrada, como identificar en qué países se le paga mejor considerando 
           el monto en dólares.
        '''),
        dcc.Graph(
            id = 'g6',
            figure = graf6
        ),
        dcc.Graph(
            id = 'g7',
            figure = graf7
        ),
        #Tercer bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
                     Nicolás: \n
        '''),html.Div(children = '''
                     Sofía: \n
        '''),html.Div(children = '''
                     Victor: \n
        '''),
        ]),
    #Escenario 4 codigo
        
        html.H3(children = 'ESCENARIO 4'),
        html.Div(children = '''
           Analizar de que forma varian los salarios según la proporción de trabajo 
           remoto que se tiene, con el objetivo de identificar que opción es mejor 
           para el trabajador, teniendo en cuenta la cantidad de empleos remotos 
           ofertados y la diferencia de ingresos. Todo esto tomando en cuenta 
           después que los trabajos presenciales implican más costos de vida y 
           limitaciones para los empleados.
        '''),
        dcc.Graph(
            id = 'g8',
            figure = graf8
        ),
        dcc.Graph(
            id = 'g9',
            figure = graf9
        ),
        #Cuarto bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
                     Nicolás: \n
        '''),html.Div(children = '''
                     Sofía: \n
        '''),html.Div(children = '''
                     Victor: \n
        '''),
        ]),
    #Escenario 5 codigo
        
        html.H3(children = 'ESCENARIO 5'),
        html.Div(children = '''
           Identificar mediante el nombre de los cargos en cuales sectores de la ciencia
            de datos se tiene una mejor expectativa salarial y observar si existe una
            diferencia significativa entre cargos asociados 
        '''),
        dcc.Graph(
            id = 'g10',
            figure = graf10
        ),
        #Quinto bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
                     Nicolás: \n
        '''),html.Div(children = '''
                     Sofía: \n
        '''),html.Div(children = '''
                     Victor: \n
        '''),
        ]),
        
    #Escenario 6 codigo
        
        html.H3(children = 'ESCENARIO 6'),
        html.Div(children = '''
           Identificar mediante el nombre de los cargos en cuales sectores de la ciencia
            de datos se tiene una mejor expectativa salarial y observar si existe una
            diferencia significativa entre cargos asociados 
        '''),
        html.H4(children = 'Promedios por años'),
        dcc.Graph(
            id = 'g11',
            figure = graf11
        ),
        html.H4(children = 'Promedios por nivel de experiencia'),
        dcc.Graph(
            id = 'g12',
            figure = graf12
        ),
        dcc.Graph(
            id = 'g13',
            figure = graf13
        ),
        dcc.Graph(
            id = 'g14',
            figure = graf14
        ),
        dcc.Graph(
            id = 'g15',
            figure = graf15
        ),
        #Sexto bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
                     Nicolás: \n
        '''),html.Div(children = '''
                     Sofía: \n
        '''),html.Div(children = '''
                     Victor: \n
        '''),
        ]),
        #Conclusiones finales
        html.Div(children=[
            html.H2(children = 'Conclusiones:'),
            html.Div(children = '''
                     Nicolás: \n
        '''),html.Div(children = '''
                     Sofía: \n
        '''),html.Div(children = '''
                     Victor: \n
        '''),
        ]),
    ],
)

    if __name__ == '__main__':
            app.run_server(debug = False)
except Exception as ex:
    print (ex)
finally: 
    connection.close()
    print("Conexiòn finalizada")
