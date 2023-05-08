from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
import os
import io
import database as db
import sys
from experta import *
import json
import matplotlib.pyplot as plt #Gráficas
import matplotlib.ticker as ticker
import numpy as np
import base64
import seaborn as sns
import pandas as pd

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src','templates')

# Agregar la ruta de la carpeta sistema_experto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
#importamos archivo del SE
from SE.sistemaExperto import Diagnostico, Sintomas

#inicializar flask, le indicamos en qué carpeta está el archivo html, y lo muestre en pantalla
app = Flask(__name__, template_folder = template_dir)
app.secret_key = 'clave_secreta' 

#Rutas de la aplicación
@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/test.html')
def test():
    IDTest = session.get('IDTest')
    
    return render_template('test.html', IDTest=IDTest)

@app.route('/estudiante.html')
def estudiante():
    
    return render_template('estudiante.html')

@app.route('/administrador.html')
def administrador():
    
    return render_template('administrador.html')

@app.route('/administrador.html')
def admin():
    
    mensaje = request.args.get("mensaje", "")
    return render_template('administrador.html',mensaje=mensaje)

@app.route('/datos.html')
def datos():
    
    return render_template('datos.html')

#Ruta para guardar usuarios en la bdd
@app.route('/estudiante', methods=['POST'])
def addEstudiante():
    # Obtenemos los datos del formulario
    IDTest = request.form['campo-autoincrementable']
    IDEstudiante = request.form['IDEstudiante']
    PrimerNombre = request.form['PrimerNombre']
    SegundoNombre = request.form['SegundoNombre']
    PrimerApellido = request.form['PrimerApellido']
    SegundoApellido = request.form['SegundoApellido']
    Edad = request.form['Edad']
    ProgramaAcademico = request.form['ProgramaAcademico']
    Semestre = request.form['Semestre']
        
    #accedemos a la base de datos
    cursor = db.database.cursor()
    sql = "INSERT INTO registrotest (IDTest, IDEstudiante, PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido, Edad, ProgramaAcademico, Semestre) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (IDTest, IDEstudiante, PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido, Edad, ProgramaAcademico, Semestre)
    cursor.execute(sql, data)
    # se realiza commit a la bdd para materializar la consulta
    db.database.commit()
    session['IDTest'] = IDTest
    return redirect(url_for('test'))

#Ruta para iniciar sesión admin
@app.route('/admin', methods=['POST'])
def loginAdmin():
    # Obtenemos los datos del formulario
    Usuario = request.form['Usuario']
    Clave = request.form['Clave']
        
    #accedemos a la base de datos
    cursor = db.database.cursor()
    sql = "SELECT * FROM administrador WHERE Usuario=%s AND Clave=%s"
    data = (Usuario,Clave)
    cursor.execute(sql, data)
    resultado = cursor.fetchone()
    
    if(resultado):
        return redirect(url_for('datos'))   
    else:
        return redirect(url_for('admin',mensaje="Error de autenticación"))

#Ruta para guardar resultado de test en la bdd
@app.route('/resultTest')
def resultTest():
    # Obtenemos los datos del formulario
    IDTest = session.get('IDTest')
    resultado = session.get('resultado')
    
    if(resultado=='["Depresión", "Ansiedad", "Estrés Agudo"]'):
        resultado="Depresión, ansiedad y estrés agudo"
    elif(resultado=='["Depresión", "Ansiedad"]'):
        resultado="Depresión y ansiedad"
    elif(resultado=='["Depresión", "Estrés Agudo"]'):
        resultado="Depresión y estrés agudo"
    elif(resultado=='["Ansiedad", "Estrés Agudo"]'):
        resultado="Ansiedad y estrés agudo"
    elif(resultado=='["Ansiedad"]'):
        resultado="Ansiedad"
    elif(resultado=='["Depresión"]'):
        resultado="Depresión"
    elif(resultado=='["Estrés Agudo"]'):
        resultado="Estrés agudo"
    elif(resultado=='["No se ha detectado ningún trastorno emocional"]'):
        resultado="Ninguno"
    
    #accedemos a la base de datos
    cursor = db.database.cursor()
    sql = "UPDATE registrotest SET Resultado_test = %s WHERE IDTest=%s"
    data = (resultado, IDTest)
    cursor.execute(sql, data)
    # se realiza commit a la bdd para materializar la consulta
    db.database.commit()

# Definimos una función que envía las respuestas al sistema experto
def enviar_respuestas(answers):
    engine = Diagnostico(cont_depresion=0,cont_ansiedad=0,cont_estres=0)
    engine.reset() # Reinicia el sistema experto antes de enviar nuevas respuestas
    engine.declare(Sintomas(cont_depresion=answers[0],cont_ansiedad=answers[1],cont_estres=answers[2])) # Agrega las respuestas como hechos al sistema experto
    engine.run() # Ejecuta el sistema experto
    resultado = engine.resultado
    resultado_json = json.dumps(resultado, ensure_ascii=False)
    recomendaciones = engine.recomendaciones
    recomendaciones_json = json.dumps(recomendaciones, ensure_ascii=False)
    return{'resultado': resultado_json,'recomendaciones': recomendaciones_json}

#ruta para mandar las respuestas del test a la bdd
@app.route('/answers', methods=['POST'])
def handle_answers():
    # Obtener las respuestas enviadas por el cliente
    answers = request.get_json()['answers']
    IDTest = request.get_json()['IDTest']
    # Enviar las respuestas al sistema experto
    respuesta = enviar_respuestas(answers)
    resultado = respuesta['resultado']
    recomendaciones = respuesta['recomendaciones']
    session['resultado'] = resultado
    session['IDTest'] = IDTest
    resultTest()
    # Enviar la respuesta al cliente
    return jsonify({'message': resultado,'recomendaciones': recomendaciones})

#ruta para generar gráficas
@app.route('/grafica', methods=['POST'])
def generar_graficas():
    # Obtenemos los datos del formulario
    ProgramaAcademico = request.get_json()['ProgramaAcademico']
    Semestre = request.get_json()['Semestre']
    #accedemos a la base de datos
    cursor = db.database.cursor()
    
    sql = "SELECT Resultado_test, COUNT(*) AS Cantidad FROM registrotest WHERE ProgramaAcademico=%s AND Semestre=%s GROUP BY Resultado_test"
    data = (ProgramaAcademico,Semestre)
    cursor.execute(sql, data)
    data1 = cursor.fetchall() 
    
    if(data1):
        # Procesar los datos y crear la gráfica
        df = pd.DataFrame(data1, columns=['Resultado_test', 'Cantidad'])
        
        sns.set(style='whitegrid', font_scale=6, font='sans-serif', rc={'font.weight': 'bold'})
        plt.figure(figsize=(35, 25))
        ax = sns.barplot(y='Resultado_test', x='Cantidad', data=df, orient='horizontal', color='fuchsia')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.set(ylabel='',xlabel='Cantidad')
        plt.tight_layout()
        
        # Guardar la gráfica en un archivo temporal
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        
        # Renderizar la plantilla HTML con la gráfica
        return jsonify({'img':base64.b64encode(img.getvalue()).decode()})
    else:
        return jsonify({'error':"No hay datos suficientes"})

#ruta para generar gráficas
@app.route('/grafica1', methods=['POST'])
def generar_graficas1():
    # Obtenemos los datos del formulario
    ProgramaAcademico = request.get_json()['ProgramaAcademico']
    Edad = request.get_json()['Edad']
    
    #accedemos a la base de datos
    cursor = db.database.cursor()
    
    sql = "SELECT Resultado_test, COUNT(*) AS Cantidad FROM registrotest WHERE ProgramaAcademico=%s AND Edad=%s GROUP BY Resultado_test"
    data = (ProgramaAcademico,Edad)
    cursor.execute(sql, data)
    data1 = cursor.fetchall()  
    
    if(data1):  
        # Procesar los datos y crear la gráfica
        df = pd.DataFrame(data1, columns=['Resultado_test', 'Cantidad'])
        
        sns.set(style='whitegrid', font_scale=6, font='sans-serif', rc={'font.weight': 'bold'})
        plt.figure(figsize=(35, 25))
        ax = sns.barplot(y='Resultado_test', x='Cantidad', data=df, orient='horizontal', color='fuchsia')
        ax.set(ylabel='',xlabel='Cantidad')
        plt.tight_layout()
        
        # Guardar la gráfica en un archivo temporal
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        
        # Renderizar la plantilla HTML con la gráfica
        return jsonify({'img':base64.b64encode(img.getvalue()).decode()})
    else:
        return jsonify({'error':"No hay datos suficientes"})
        
#lanzamos la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=4500)