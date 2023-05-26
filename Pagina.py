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
    graf6 = px.histogram(rows, x = 1,y = 3 , pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Salario promedio por título de trabajo en nivel de entrada")
    graf7 = px.histogram(rows, x = 2,y = 3, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Cantidad de empleos por tipo en nivel de entrada")

    #ESCENARIO 4
    cursor.execute('''select promocion_remoto, count(*), round(avg(salario_usd),2)
    from empleo
    group by promocion_remoto;''')
    rows = cursor.fetchall()
    graf8 = px.histogram(rows, x = 0,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Salario promedio por título de trabajo en nivel de entrada")
    graf9 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Cantidad de tipo de empleo en nivel de entrada")

    #ESCENARIO 5
    cursor.execute('''select promocion_remoto, count(*), round(avg(salario_usd),2)
    from empleo
    group by promocion_remoto;''')
    rows = cursor.fetchall()
    graf8 = px.histogram(rows, x = 0,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Salario promedio por título de trabajo en nivel de entrada")
    graf9 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Cantidad de tipo de empleo en nivel de entrada")

    #ESCENARIO 6
    cursor.execute('''select promocion_remoto, count(*), round(avg(salario_usd),2)
    from empleo
    group by promocion_remoto;''')
    rows = cursor.fetchall()
    graf8 = px.histogram(rows, x = 0,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Salario promedio por título de trabajo en nivel de entrada")
    graf9 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Cantidad de tipo de empleo en nivel de entrada")


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
    ],
)

    if __name__ == '__main__':
            app.run_server(debug = False)
except Exception as ex:
    print (ex)
finally: 
    connection.close()
    print("Conexiòn finalizada")
