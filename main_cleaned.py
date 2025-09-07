from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import random
from pathlib import Path

app = FastAPI()

qa_data = []

def load_qa():
    global qa_data
    path = Path("qa.json")
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            qa_data.clear()
            qa_data.extend(json.load(f))

load_qa()

@app.get("/domande")
def get_all_qa():
    return qa_data

@app.get("/domanda/{index}")
def get_qa(index: int):
    if 0 <= index < len(qa_data):
        return qa_data[index]
    return {"errore": "Indice non valido"}

@app.get("/random")
def get_random_qa():
    return random.choice(qa_data)

# ----------------------------
# NUOVE ROTTE PER GESTIONE QUIZ MULTIPLI
# ----------------------------

@app.get("/quiz/{quiz_name}")
def get_quiz(quiz_name: str):
    """Carica un quiz in base al nome (es: /quiz/pompiere -> multiple_choice_pompiere.json)."""
    file_path = Path(f"multiple_choice_{quiz_name}.json")
    if not file_path.exists():
        return {"errore": f"Quiz '{quiz_name}' non trovato."}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/menu", response_class=HTMLResponse)
def menu():
    """Mostra una pagina di menu per scegliere il quiz."""
    html = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
      <meta charset="UTF-8">
      <title>Seleziona Quiz</title>
    </head>
    <body>
      <h1>Scegli il tuo quiz</h1>
      <ul>
            <li><a href="/quiz/pompiere">Quiz Pompiere</a></li>
             <li><a href="/quiz/generale">Quiz Generale</a></li>
            <li><a href="/quiz/primo_soccorso">Quiz Primo Soccorso</a></li>
             <li><a href="/quiz/competenze">Quiz Competenze Digitali</a></li>
      </ul>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ----------------------------
# HOME PAGE (vecchia index)
# ----------------------------

@app.get("/", response_class=HTMLResponse)
def index():
    with open("template.html", encoding="utf-8") as f:
        return f.read()
