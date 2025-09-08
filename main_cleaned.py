from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import uvicorn
import os

app = FastAPI()

# Percorsi dei file JSON per i due quiz
QUIZ_1_PATH = "multiple_choice.json"
QUIZ_2_PATH = "multiple_choice_2.json"

# Percorso per i template HTML
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Schermata iniziale con due pulsanti per i quiz."""
    return templates.TemplateResponse("template.html", {
        "request": request,
        "title": "Seleziona un quiz",
        "quiz1_label": "Avvia Quiz",
        "quiz2_label": "Avvia Quiz 2"
    })

@app.get("/quiz", response_class=JSONResponse)
async def get_quiz():
    """Restituisce le domande del primo quiz."""
    if os.path.exists(QUIZ_1_PATH):
        with open(QUIZ_1_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"title": "Quiz Originale", "questions": data}
    return {"error": "File delle domande non trovato."}

@app.get("/quiz2", response_class=JSONResponse)
async def get_quiz2():
    """Restituisce le domande del secondo quiz."""
    if os.path.exists(QUIZ_2_PATH):
        with open(QUIZ_2_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"title": "Quiz Competenze Digitali", "questions": data}
    return {"error": "File delle domande non trovato."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
