from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import psycopg2

try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'DataScientists'
    )
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select promocion_remoto, count(*), round(avg(salario_usd),2) from empleo group by promocion_remoto")
    rows = cursor.fetchall()
    app = Dash(__name__)
    fig = px.bar(rows, x = 0, y = 1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "productos por editorial")
    app.layout = html.Div(children = [
        html.H1(children = 'Gráfico Edición Cantidad'),
        html.Div(children = '''
            Dash: Aplicación para graficar fatos
        '''),
        dcc.Graph(
            id = 'Example-Graph',
            figure = fig
        ),dcc.Input(id='input', placeholder='Escribe algo aqui!', type='text'),
    html.Div(id='output')
        
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
    @app.callback(
            Output(component_id='output', component_property='children'),
            [Input(component_id='input', component_property='value')]
    )
    def update_value(input_data):
            return 'Input: "{}"'.format(input_data)
    if __name__ == '__main__':
            app.run_server(debug = False)
except Exception as ex:
    print (ex)
finally: 
    connection.close()
    print("Conexiòn finalizada")
