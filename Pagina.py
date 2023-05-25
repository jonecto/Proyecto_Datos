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