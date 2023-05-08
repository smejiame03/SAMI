const quizData = [
    {
        question: "Presenta estado de animo deprimido (se siente triste, vacío, sin esperanza) la mayor parte del día o casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Tiene disminución importante del interés o el placer por todas o casi todas las actividades la mayor parte del día, casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Tiene pérdida importante de peso sin hacer dieta o aumento de peso, o disminución o aumento del apetito casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta insomnio (dificultad para conciliar el sueño) o hipersomnia (excesivamente somnoliento) casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Tiene agitación o retraso psicomotor (inquietud o enlentecimiento) casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta fatiga o pérdida de energía casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta sentimiento de inutilidad o culpabilidad excesiva o inapropiada casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Tiene pensamientos de muerte recurrentes, ideas suicidas recurrentes sin un plan determinado, intento de suicidio o un plan específico para llevarlo a cabo:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Tiene dificultad para pensar o concentrarse, o para tomar decisiones, casi todos los días:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Siente inquietud o sensación de estar atrapado o con los nervios de punta:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Se siente fácilmente fatigado o cansado:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta irritabilidad:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta tensión muscular:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta problemas de sueño (dificultad para dormirse o para continuar durmiendo, o sueño inquieto e insatisfactorio):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Ha estado expuesto a un acotecimiento traumático en el que haya experimentado o presenciado muertes o amenazas para su integridad física o la de los demás, y ha respondido con temor, desesperanza u horror intenso:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta recuerdos angustiosos recurrentes, involuntarios e intrusivos del suceso(s) traumático(s):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta sueños angustiosos recurrentes en los que el contenido y/o el afecto del sueño está relacionado con el suceso(s):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta reacciones disociativas en las que siente o actúa como si se repitiera el suceso(s) traumático(s) (p. ej., pérdida de consciencia del entorno presente):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta malestar psicológico intenso o prolongado al exponerse a factores que se parecen a un aspecto del acontecimiento traumático:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Se siente incapaz de recordar un aspecto importante del suceso(s) traumático(s) (que no se deba a factores como una lesión cerebral, alcohol o drogas):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Realiza esfuerzos para evitar recuerdos, pensamientos o sentimientos angustiosos acerca o estrechamente asociados al suceso(s) traumático(s):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Realiza esfuerzos para evitar recordatorios externos (personas, lugares, conversaciones, actividades, objetos, situaciones) que despiertan recuerdos, pensamientos o sentimientos angustiosos acerca o estrechamente asociados al suceso(s) traumático(s):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta incapacidad persistente de experimentar emociones positivas (p. ej., felicidad, satisfacción o sentimientos amorosos):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta sentido de la realidad alterado del entorno o de usted mismo (p. ej., verse uno mismo desde la perspectiva de otro, estar pasmado, lentitud del tiempo):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta arrebatos de furia (con poca o ninguna provocación) que se expresa típicamente como agresión verbal o física contra personas u objetos:",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta hipervigilancia (sentirse alerta a cualquier peligro oculto de la gente o de su entorno, normalmente estos peligros no son reales):",
        a: "Sí",
        b: "No",
    },
    {
        question: "Presenta respuesta de sobresalto exagerada (contracción muscular rápida e involuntaria de los musculos faciales y de las extremidades provocada por un estímulo repentino):",
        a: "Sí",
        b: "No",
    },
];
const quiz= document.getElementById('quiz')
const answerEls = document.querySelectorAll('.answer')
const questionEl = document.getElementById('question')
const a_text = document.getElementById('a_text')
const b_text = document.getElementById('b_text')
const submitBtn = document.getElementById('submit')
let currentQuiz = 0

loadQuiz()
function loadQuiz() {
    deselectAnswers()
    const currentQuizData = quizData[currentQuiz]
    questionEl.innerText = currentQuizData.question
    a_text.innerText = currentQuizData.a
    b_text.innerText = currentQuizData.b
}
function deselectAnswers() {
    answerEls.forEach(answerEl => answerEl.checked = false)
}
function getSelected() {
    let answer
    answerEls.forEach(answerEl => {
        if(answerEl.checked) {
            answer = answerEl.id
        }
    })
    return answer
}

// Creamos lista para acumular las respuestas
var answers = [];
var IDTest = 0;
var cont1=0;
var cont2=0;
var cont3=0;

submitBtn.addEventListener('click', () => {
    // Obtener la respuesta seleccionada por el usuario
    const answer =  getSelected()
    if(answer){
        currentQuiz++
        if(currentQuiz==15){
            if(answer=='Sí'){
                cont3++
                loadQuiz()
            }else{
                currentQuiz=22
                loadQuiz()
            }
        }
        if(currentQuiz < quizData.length) {
            if(currentQuiz<9){
                if(answer=='Sí'){
                    cont1++
                    loadQuiz()
                }else{
                    loadQuiz()
                }
            }
            else if(currentQuiz==9){
                if(answer=='Sí'){
                    cont1++
                    cont2++
                    cont3++
                    loadQuiz()
                }
                else{
                    loadQuiz()
                }
            }
            else if(currentQuiz>9 & currentQuiz<14){
                if(answer=='Sí'){
                    cont2++
                    loadQuiz()
                }else{
                    loadQuiz()
                }
            }
            else if(currentQuiz==14){
                if(answer=='Sí'){
                    cont2++
                    cont3++
                    loadQuiz()
                }else{
                    loadQuiz()
                }
            }
            else if(currentQuiz>14 & currentQuiz<=27){
                if(answer=='Sí'){
                    cont3++
                    loadQuiz()
                }else{
                    loadQuiz()
                }
            }
        } else {
            // Agregar la respuesta
            answers.push(cont1,cont2,cont3);
            // Tomamos el IDTest
            IDTest = document.getElementById("IDTest").value;
            // Hacer una solicitud POST al servidor Flask con todas las respuestas
            fetch('/answers', {
                method: 'POST',
                body: JSON.stringify({answers: answers,IDTest: IDTest}),
                headers: {
                'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                
                if(data.message!=='["No se ha detectado ningún trastorno emocional"]'){
                    quiz.innerHTML = `
                    <div class="service">
                        <h3>Los posibles trastornos emocionales identificados son: </h3><br>
                        <h3 class="n-service">${JSON.parse(data.message).join(", ")}</h3>
                    </div>
                    <div class="service">
                        <h3>Te sugerimos seguir las siguientes recomendaciones: </h3><br>
                        <p>${data.recomendaciones}</p>
                    </div>
                    <h3>Además, te sugerimos asignar una cita con un especialista en el tema, puedes hacerlo ingresando al siguiente enlace: </h3><br>
                    <a aria-label="Chat on WhatsApp" href="https://wa.me/573003927598?text=Quiero%20solicitar%20una%20cita%20con%20la%20psicóloga"><img style="display: block; margin: auto; width:50%;" alt="Chat on WhatsApp" src="../static/images/WhatsAppButtonGreenLarge.png"/></a>
                    <br>
                    <footer>
                        <div class="contenedor footer-content">
                            <h4><span class="sami">NOTA.</span> El diagnóstico proporcionado por este sistema experto es sólo una herramienta y no reemplaza la atención de un especialista médico. Le recomendamos que consulte con un médico o profesional de la salud mental.</h4>
                        </div>
                        <div class="line"></div>
                    </footer>
                    <br><button onclick="location.href='/'">Regresar al inicio</button>`
                }
                else{
                    quiz.innerHTML = `
                    <div class="service">
                        <h3>Resultado obtenido: </h3><br>
                        <h3 class="n-service">${JSON.parse(data.message).join(", ")}</h3>
                    </div>    
                    <footer>
                        <div class="contenedor footer-content">
                            <h4><span class="sami">NOTA.</span> El diagnóstico proporcionado por este sistema experto es sólo una herramienta y no reemplaza la atención de un especialista médico. Le recomendamos que consulte con un médico o profesional de la salud mental.</h4>
                        </div>
                        <div class="line"></div>
                    </footer>
                    <br><h3>Si deseas asignar una cita con un especialista en el tema, puedes hacerlo ingresando al siguiente enlace: </h3><br>
                    <a aria-label="Chat on WhatsApp" href="https://wa.me/573003927598?text=Quiero%20solicitar%20una%20cita%20con%20la%20psicóloga"><img style="display: block; margin: auto; width:50%;" alt="Chat on WhatsApp" src="../static/images/WhatsAppButtonGreenLarge.png"/></a>
                    <br>
                    <br><button onclick="location.href='/'">Regresar al inicio</button>`
                }
            })
        }
    }
})