from experta import *
from flask import Flask, jsonify

#creamos las variables
lista_enfermedades = []
lista_sintomas = []
enfermedades1 = {}
recomendaciones = {}

diagnosticos = open(r"flask/src/SE/Diagnosticos.txt", mode='r', encoding='utf-8-sig')
diagnosticos_t = diagnosticos.read()
lista_diagnosticos = diagnosticos_t.split("\n")
diagnosticos.close()

for enfermedad in lista_diagnosticos:
    archivo_recomendaciones = open(r"flask/src/SE/Recomendaciones/"+enfermedad+".txt",encoding='utf-8-sig')
    datos_recomendaciones = archivo_recomendaciones.read()
    recomendaciones[enfermedad] = datos_recomendaciones
    archivo_recomendaciones.close()
    
#generando clase para la base de conocimiento
class Sintomas(Fact):
    """Información de trastornos"""
    pass

class Diagnostico(KnowledgeEngine):
    def __init__(self, cont_depresion, cont_ansiedad, cont_estres):
        super().__init__()
        self.cont_depresion = cont_depresion
        self.cont_ansiedad = cont_ansiedad
        self.cont_estres = cont_estres
        self.resultado = None
        self.recomendaciones = None
        
    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion >= 5), TEST(lambda cont_ansiedad: cont_ansiedad >=3), TEST(lambda cont_estres: cont_estres >= 10))
    def disease_0(self):
        resultados = ["Depresión", "Ansiedad", "Estrés Agudo"]
        self.resultado = resultados
        self.recomendaciones = recomendaciones['depresion_ansiedad_estresAgudo']
        
    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion >= 5), TEST(lambda cont_ansiedad: cont_ansiedad <3), TEST(lambda cont_estres: cont_estres < 10))
    def disease_1(self):
        resultados = ["Depresión"]
        self.resultado = resultados
        self.recomendaciones = recomendaciones['depresion']
        
    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion >=5), TEST(lambda cont_ansiedad: cont_ansiedad >=3), TEST(lambda cont_estres: cont_estres < 10))
    def disease_2(self):
        resultados = ["Depresión", "Ansiedad"]
        self.resultado = resultados
        self.recomendaciones = recomendaciones['depresion_ansiedad']
    
    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion >= 5), TEST(lambda cont_ansiedad: cont_ansiedad <3), TEST(lambda cont_estres: cont_estres >=10))
    def disease_3(self):
        resultados = ["Depresión", "Estrés Agudo"]
        self.resultado = resultados
        self.recomendaciones = recomendaciones['depresion_estresAgudo']

    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion <5), TEST(lambda cont_ansiedad: cont_ansiedad >=3), TEST(lambda cont_estres: cont_estres <10))
    def disease_4(self):
        resultados = ["Ansiedad"]
        self.resultado = resultados
        self.recomendaciones = recomendaciones['ansiedad']
        
    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion <5), TEST(lambda cont_ansiedad: cont_ansiedad >=3), TEST(lambda cont_estres: cont_estres >=10))
    def disease_5(self):
        resultados = ["Ansiedad", "Estrés Agudo"]
        self.resultado = resultados
        self.recomendaciones = recomendaciones['ansiedad_estresAgudo']
        
    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion <5), TEST(lambda cont_ansiedad: cont_ansiedad <3), TEST(lambda cont_estres: cont_estres >=10))
    def disease_6(self):
        resultados = ["Estrés Agudo"]
        self.resultado = resultados
        self.recomendaciones = recomendaciones['estresAgudo']
        
    @Rule(Sintomas(cont_depresion=MATCH.cont_depresion,cont_ansiedad=MATCH.cont_ansiedad,cont_estres=MATCH.cont_estres), TEST(lambda cont_depresion: cont_depresion <5), TEST(lambda cont_ansiedad: cont_ansiedad <3), TEST(lambda cont_estres: cont_estres <10))
    def disease_7(self):
        resultados = ["No se ha detectado ningún trastorno emocional"]
        self.resultado = resultados