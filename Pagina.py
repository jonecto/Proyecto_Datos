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
    fig = px.bar(rows, x = 0, y = 1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "numero de datos por proporcion de trabajo remoto")
   
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
    graf6 = px.histogram(rows, x = 1,y = 3 , pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Salario promedio por título de trabajo para Entry")
    graf7 = px.histogram(rows, x = 2,y = 3, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Cantidad de empleos por tipo en capacitación Entry")

    #ESCENARIO 4
    cursor.execute('''select promocion_remoto, count(*), round(avg(salario_usd),2)
    from empleo
    group by promocion_remoto;''')
    rows = cursor.fetchall()
    graf8=fig = px.bar(rows, x = 0,y=2, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "Promedio de salario por modalidad en nivel de entrada")
    graf9 = px.pie(rows, values=1, names=0, title='Cantidad de empleos por modalidad en nivel de entrada')

    #ESCENARIO 5
    cursor.execute('''SELECT nombre_trabajo, round(count(*),1) AS cantidad_empleos
    FROM empleo
    GROUP BY nombre_trabajo
    ORDER BY cantidad_empleos DESC
    LIMIT 5;''')
    rows = cursor.fetchall()
    graf10 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "top 5 empleos mas demandados (Cantidad).")

    cursor.execute('''SELECT nombre_trabajo, round(avg(salario_usd),1) AS cantidad_empleos
    FROM empleo
    GROUP BY nombre_trabajo
    ORDER BY cantidad_empleos DESC
    LIMIT 5;''')
    rows = cursor.fetchall()
    graf11 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "top 5 empleos con mejor promedio de salario.")


    cursor.execute('''Select 'Ingeiero de datos' as Nombre_trabajo, ROUND(AVG(salario_usd), 1) AS Salario_promedio
    from empleo
    where nombre_trabajo LIKE '%Data Engineer%'
    union
    select 'Cientifico de datos' AS Nombre_trabajo, ROUND(AVG(salario_usd), 1) AS Salario_promedio
    from empleo
    where nombre_trabajo LIKE '%Data Scientist%'
    union
    select 'Analista de datos' AS Nombre_trabajo, ROUND(AVG(salario_usd), 1) AS Salario_promedio
    from empleo
    where nombre_trabajo LIKE '%Analyst%';''')
    rows = cursor.fetchall()
    graf12 = px.histogram(rows, x = 0,y=1, pattern_shape = 1, pattern_shape_sequence = ['\\', '.', '+', '/', '.'], color_discrete_sequence = ["#34a0a4"], title = "promedio salarios de las tres profesiones màs importantes")

    #ESCENARIO 6
    cursor.execute('''select nivel_experiencia, anio,
        round(avg(salario_usd), 1) salario_promedio 
        from empleo
        group by nivel_experiencia, anio
        order by nivel_experiencia;''')
    rows = cursor.fetchall()
    graf13 = px.line(rows, x = 0,y=2, color=1)
    
    cursor.execute('''select anio, tipo_empleo,
    round(avg(salario_usd), 1) AS Salario_promedio
    from empleo
    group by anio, tipo_empleo
    order by anio, tipo_empleo;''')
    rows = cursor.fetchall()
    print(rows)
    graf14 = px.line(rows, x = 1,y=2, color=0)
    


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
                     Sofía: Las empresas donde más ganan los trabajadores son las medianas,
		     sin una diferencia tan significativa con las grandes que las siguen. 
		     Por otra parte los 5 países donde se obtienen mejores salarios son Israel,
		     Puerto Rico, Estados Unidos, Rusia, Canadá y Nueva Zelanda, de esta información
		     se puede destacar que 3 de ellos se encuentran en América, sea central o del norte. 
        '''),' ',html.Div(children = '''
                     Victor: A la luz de la primera gráfica se puede asegurar que el lugar donde se 
                     sitúan las empresas sí influye en los salarios pagados a los trabajadores de la
                     industria de la ciencia de datos. El hecho de que no sea una distribución 
                     uniforme muestra que en países con industrias de software más desarrolladas pagan
                     mejor. Paises como Israel, Canada o EE.UU.
		     
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
                     Sofía: Los más frecuentes y mejor remunerados resultan ser los 
		     trabajos dados para el nivel de experiencia Senior. Lo cual indica
		     que es el nivel de experiencia más solicitado por las empresas y el
		     cual es económicamente más beneficioso para los trabajadores.
        '''),html.Div(children = '''
                     Victor: 
                     Más del 60% de los cientificos de datos de las empresas son de 
                     nivel senior. Así mismo, al pago los trabajadores con este nivel 
                     es a donde las empresas destinan más dinero. 
                     El hecho de que, pese a haber casi la misma cantidad de empleados con
                     nivel Entry (practicantes o junior) que de empleados con nivel Mid, 
                     las empresas destinen el mismo dinero a ambos niveles deja ver lo mal
                     remunerados en relativo que están los entry. 
		     
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
                     Sofía:Las mejore expectativas para nivel de entrada de dan para “Científicos aplicados” y lo
		     más probable es obtener un puesto de tiempo completo. 
        '''),' ',html.Div(children = '''
                     
		     Victor:
                     Pese a que si son los empleados menos pagados, los trabajadores de nivel entry pueden 
                     llegar a tener salario muy buenos. Pero para llegar a tener los mejores salarios, la gente
                     que quiere entrar a la industria de la ciencia de datos deberá adquirir cococimientos muy 
                     especificos y epecializaciados como el machine learning, la vision automática o el deep learning.
                     Afortunadamente, la gran mayoría de empleos ofrecidos a la gente entrante es FT(tiempo completo).
    
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
generalmente es muy cercana (ambas están alrededor de los 1200 empleos ofertados). Además de esto 
se puede observar una clara diferencia con las personas que tienen emoleos mixtos, puesto que
sus salarios son bastante bajos y no hay mucha oferta en estos tipos de empleo.
        '''),' ',html.Div(children = '''
                     Sofía:Las diferencias entre la agrupación de modalidades mixta y presencial y
		     los trabajos presenciales es insignificante. Aunque los salarios en promedio
		     de la modalidad virtual y de la modalidad remota se notan similares y mayores
		     a aquellos en modalidad mixta.
        '''),' ',html.Div(children = '''
                     Victor: Los gráficos revelan las preferencias/posibilades de las empresas. 
                     Seguramente los trabajos mixtos sean operacionalmente más costos y esto explicaría
                     que los empleos con proporción remota de 50% sean los menos ofrecidos.
                     
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
        dcc.Graph(
            id = 'g11',
            figure = graf11
        ),
        dcc.Graph(
            id = 'g12',
            figure = graf12
        ),
        #Quinto bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
                     Nicolás: 
            Se puede evidenciar dentro de las gráficas 
            que los empleos más demandados generalmente 
            aquellos que requieren mucha más preparación, como lo es
            el ingeniero de Machine Learning, o el Ingeniero de Datos. Adicional a esto 
            se puede observar que los empleos mejor remunerados son aquellos 
            que implican alguna clase de liderazgo, sea anejo de proyectos como el 
            cientifico de datos principal o lider de areas como el lider de analistas de datos.
        '''),' ',html.Div(children = '''
                     Sofía:Los salarios con más disponibilidad de empleo son para títulos de empleo con
		     relación a la ingeniería, como por ejemplo “Ingeniero de datos”, “Ingeniero de 
		     Aprendizaje de Máquina” e “Ingeniero de análisis”. Pero, por otra parte, los títulos
		     de empleo que más dinero ganan en promedio son aquellos que se relacionan con el liderazgo.
		     Los que aparecen en ambos gráficos son los “Analistas de datos” y “Científicos de datos”. 
        '''),' ',html.Div(children = '''
                     Victor: 
                     En la realidad el nombre del empleo solo permite hacerse una idea muy general
                     y podría ser imprecisa, ya que no conocemos las funciones y hacerses de cada cargo. El 
                     nombre puede significar cosas distintas entre distintas empresas. Por ejemplo un data 
                     scientist también debe tener capacidad de análisis y saber de machine learning.
                     Dicho esto, justamente los tres empelos que en la industria son los quen en nuestra base 
                     de datos son los más demandados: Ingeniero de datos, cientifico de datos y analista de 
                     datos. Y también la distribución salarial es la eseperada; de los tres, el que mas gana
                     es el ingeniero y el que menos es el analista, aunque la diferencia no es significativa
                     
        '''),
        ]),
        
    #Escenario 6 codigo
        
        html.H3(children = 'ESCENARIO 6'),
        html.Div(children = '''
           Identificar mediante el nombre de los cargos en cuales sectores de la ciencia
            de datos se tiene una mejor expectativa salarial y observar si existe una
            diferencia significativa entre cargos asociados 
        '''),
        html.H4(children = 'Promedios por nivel de experiencia'),
        dcc.Graph(
            id = 'g13',
            figure = graf13
        ),
        html.H4(children = 'Promedios por tipo de empleo'),
        dcc.Graph(
            id = 'g14',
            figure = graf14
        ),
        
        #Sexto bloque de analisis
        html.Div(children=[
            html.H3(children = 'Análisis:'),
            html.Div(children = '''
Nicolás: Como es de esperarse, se puede observar un aumento en 
el salario promedio para cada uno de los 
niveles de experiencia, especialmente en el salario de los
senior. Con respecto a los tipos de empleo se puede decir que 
en general no hay mucha relación con los años, dada la fluctuación
grande entre fechas y la poca relación con eventos globales como 
la pandemia.
        '''),' ',html.Div(children = '''
                     Sofía: Cuando se toma la agrupación de nivel de experiencia se ve que una clara
		     tendencia a que los salarios aumentan con el transcurso del tiempo. Mientras en
		     la agrupación por tipo de empleo presenta una disminución en los salarios para el
		     año 2023. En especial para los Freelance y Contractor.
        '''),' ',html.Div(children = '''
                     Victor: Nuestra muesta tiene pocos datos de los años de la pandemia. Pero aún así
                     podemos concluir que para todos los niveles niveles de empleo, los años pospandemia
                     son mejores que los años de pandemia. La situación de los empleados sin experiencia
                     mejora considerablemente pasando de 60 mil dolares por año en pandemia a casi 100 mil
                     en 2023.
        '''),
        ]),
        
        #Conclusiones finales
        html.Div(children=[
            html.H2(children = 'Conclusiones:'),
            html.Div(children = '''
                     Nicolás: Teniendo en cuenta los datos, se puede 
                     concluir que los salarios de Cientificos de Datos son bastante promedio a
                     comparación de los salarios de otras carreras. Se puede notar también que existe una 
                     relación directa clara entre los salarios y el nivel de preparación laboral, siendo los cargos
                     ejecutivos los mejor remunerados. Adicional a esto, se puede evidenciar una gran 
                     facilidad de ingreso en este campo laboral, puesto que se ofertan bastantes empleos con salarios
                     bastante generosos para ser de un nivel de entrada. Con respecto al proyecto sentí que fue un buen 
                     ejercicio de análisis, el proceso de tratamiento de una base de datos (normalización de la base de datos, 
                     carga de datos masiva, etc) y la creación de gráficas y una página web me pareció 
                     interesante y siento que enriqueció mis conocimientos.
        '''),html.Div(children = '''
                     Sofía:Las expectativas salariales según empresa rondan el intervalo de 10.00 a 200.000 dólares y no
		     suelen superar los 100.000, lo cual como expectativa mensual es algo bajo. Por otra parte, las mejores 
		     empresas para trabajar son las medianas de los países Israel, Puerto Rico y Estados Unidos. 
	'''),html.Div(children = '''
			Según los datos vale totalmente la pena llegar al nivel de experiencia Senior a pesar del esfuerzo,
			ya que este es el más solicitado y con mejor expectativa salarial. Aunque se evidencia que los trabajos 
			de nivel de entrada son bien remunerados y tienen una gran proporción de ser de tiempo completo, lo cual 
			es positivo al aumentar los ingresos económicos.
	'''),html.Div(children = '''
			No se presenta una diferencia significativa entre la oferta de trabajos o salarios de los empleos
			remotos o mixtos con respecto a los trabajos presenciales. Aunque si se ve una diferencia de ingresos 
			negativa para los trabajos mixtos. Teniendo en cuenta que los trabajos presenciales ameritan un mayor 
			gasto para el trabajador, se considera que lo mejor es aspirar a un trabajo remoto.
	'''),html.Div(children = '''
			Agrupando los trabajos por nivel de experiencia se nota un aumento en los salarios a través 
			del tiempo lo cual indica una buena expectativa para el futuro cerca. Por otra parte, al agrupar por 
			tipo de empleo se obtienen datos desalentadores en el año 2023. Esto indica que según el nivel de 
			experiencia que se tenga el contexto es alentador pero se debe tener cuidado al considerar trabajos
			según el tipo de empleo.
        '''),html.Div(children = '''
                     Victor: Nuestra muestra tiene información valiosa a cerca del estado de la industria de la
                     ciencia de datos. A partir de esta podemos responder a la inquietud de si cómo inexpertos jóvenes
                     desarrolladores esta industria era una donde valía la pena entrar, diciendo que todos los niveles
                     de experiencia son muy bien compensados económicamente y hay gran variedad de opciones de trabajo 
                     remoto y presencial. 
                     
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
