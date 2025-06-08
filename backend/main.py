from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
from backend.evaluator import evaluate
import io
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

def get_easy_words():
    connect = sqlite3.connect("words.db")
    cursor = connect.cursor()
    cursor.execute("SELECT word FROM words WHERE difficulty = 'easy'")
    words = [row[0] for row in cursor.fetchall()]
    connect.close()
    return words

def get_medium_words():
    connect = sqlite3.connect("words.db")
    cursor = connect.cursor()
    cursor.execute("SELECT word FROM words WHERE difficulty = 'medium'")
    words = [row[0] for row in cursor.fetchall()]
    connect.close()
    return words

def get_hard_words():
    connect = sqlite3.connect("words.db")
    cursor = connect.cursor()
    cursor.execute("SELECT word FROM words WHERE difficulty = 'hard'")
    words = [row[0] for row in cursor.fetchall()]
    connect.close()
    return words

# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    words = get_easy_words()
    word = random.choice(words)
    return templates.TemplateResponse("index.html", {"request": request, "word": word})

# form post handler
@app.post("/upload", response_class=HTMLResponse)
async def post_form(request: Request, word: str = Form(...), file: UploadFile = File(...)):
    # read file and evaluate pronounciation
    file_bytes = await file.read()
    audio_file = io.BytesIO(file_bytes)
    result = evaluate(audio_file, word)
    
    return templates.TemplateResponse("index.html", {"request": request, "word": word, "result": result})
