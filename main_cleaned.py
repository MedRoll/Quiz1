from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

app = FastAPI()

qa_data = []
quiz_data = []
ordered_questions = []

def load_data():
    global qa_data, quiz_data, ordered_questions
    # carico qa.json e multiple_choice.json
    for filename, target in [("qa.json", qa_data), ("multiple_choice.json", quiz_data)]:
        path = Path(filename)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                target.clear()
                target.extend(json.load(f))

    # carico ordered_questions.json separatamente
    path_ordered = Path("ordered_questions.json")
    if path_ordered.exists():
        with open(path_ordered, "r", encoding="utf-8") as f:
            ordered_questions.clear()
            ordered_questions.extend(json.load(f))

load_data()

@app.get("/domande")
def get_all_qa():
    return qa_data

@app.get("/domanda/{index}")
def get_qa(index: int):
    if 0 <= index < len(qa_data):
        return qa_data[index]
    return {"errore": "Indice non valido"}

@app.get("/sequenza/{index}")
def get_sequenza(index: int):
    if 0 <= index < len(ordered_questions):
        return ordered_questions[index]
    return {"errore": "Indice non valido"}

@app.get("/quiz_data/{index}")
def get_quiz_data(index: int):
    if 0 <= index < len(quiz_data):
        return quiz_data[index]
    return {"errore": "Indice non valido"}

@app.get("/quiz_all")
def get_all_quiz_data():
    return quiz_data

@app.get("/", response_class=HTMLResponse)
def index():
    with open("template.html", encoding="utf-8") as f:
        return f.read()
