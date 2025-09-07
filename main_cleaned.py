from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
import random

app = FastAPI()
templates = Jinja2Templates(directory=".")

qa_data = []

def load_qa():
    global qa_data
    path = Path("qa.json")
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            qa_data.clear()
            qa_data.extend(json.load(f))

load_qa()

# ----------------------------
# Rotte per QA base
# ----------------------------

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
# Rotte per quiz multipli
# ----------------------------

@app.get("/quiz/{quiz_name}", response_class=HTMLResponse)
def get_quiz_page(request: Request, quiz_name: str):
    """Mostra il template interattivo per il quiz scelto"""
    return templates.TemplateResponse("template.html", {
        "request": request,
        "quiz_name": quiz_name
    })

@app.get("/quiz/{quiz_name}/data")
def get_quiz_data(quiz_name: str):
    """Restituisce i dati del quiz (JSON)"""
    file_path = Path("quiz") / f"multiple_choice_{quiz_name}.json"
    if not file_path.exists():
        return {"errore": f"Quiz '{quiz_name}' non trovato."}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/menu", response_class=HTMLResponse)
def menu():
    """Menu di scelta quiz"""
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

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("template.html", {
        "request": request,
        "quiz_name": "generale"  # default
    })
