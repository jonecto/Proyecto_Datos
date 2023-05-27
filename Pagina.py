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
                     Nicolás: 
                     Como se puede observar en las gráficas, la mayoría de las empresas
                     están en salarios de entre 10.000 y 200.000 dólares,
                     con muy pocas pagando más de 100.000 a sus empleados.
                     Esto muestra que el panorama laboral no es muy favorable,
                     dado que por més se ganaría alrededor de 800 dólares.
                     Sin embargo, es muy probable que estos datos vengan de freelancers por 
                     lo que se puede ver en gráficas posteriores.
        '''),' ',html.Div(children = '''
                     Sofía: 
        '''),' ',html.Div(children = '''
                     Victor: 
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
                     Nicolás: Se puede observar que 
                     los empleos de nivel ejecutivo, si bien son 
                     mejor remunerados, son muy poco frecuentes de encontrar
                     en este medio, al igual que los empleos de entrada. 
                     Pese a ser más, los niveles de entrada tienen prácticaente la 
                     misma inversión de los ejecutivos, lo que significa que 
                     son menos remunerados.
        '''),html.Div(children = '''
                     Sofía: 
        '''),html.Div(children = '''
                     Victor: 
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
                     Nicolás: Para los empleos de nivel de entrada, se puede observar que no son tan mal
                     pagados, llegando máximo a los 340.000 dólares. Se puede observar una relación entre
                     el nombre del trabajo y su complejidad con la remuneración, dado que los empleos mejor pagados
                     son aquellos que requieren mayor preparación.
        '''),html.Div(children = '''
                     Sofía: 
        '''),' ',html.Div(children = '''
                     Victor:
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
        html.H4(children='IMPORTANTE: para la visualización de los datos, el valor -50 en las gráficas representa quellos empleos que no tienen un componente de trabajo remoto.'),
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
                     Nicolás: Se puede observar que la mayoría de empleos se distribuyen 
                     en la virtualidad total o la presencialidad total, y su oferta de trabajo 
                     generalmente es muy cercana (ambas están alrededor de los 1200 empleos ofertados). 
        '''),' ',html.Div(children = '''
                     Sofía: 
        '''),' ',html.Div(children = '''
                     Victor: 
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
