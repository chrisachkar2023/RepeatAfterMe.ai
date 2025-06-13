from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
import random
from backend.evaluator import evaluate
import io
import sqlite3
from fastapi.staticfiles import StaticFiles
import base64

app = FastAPI()

# for static frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

templates = Jinja2Templates(directory="frontend")

# returns a random word from a desired difficulty
def get_random_word_by_difficulty(difficulty: str):
    connect = sqlite3.connect("backend/words.db")
    cursor = connect.cursor()
    cursor.execute("SELECT word FROM words WHERE difficulty = ?", (difficulty.lower(),))
    words = [row[0] for row in cursor.fetchall()]
    connect.close()
    return random.choice(words)

# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    word = get_random_word_by_difficulty("easy")
    return templates.TemplateResponse("index.html", {"request": request, "word": word})

# form post handler
@app.post("/upload", response_class=HTMLResponse)
async def post_form(request: Request, word: str = Form(...), file: UploadFile = File(...)):
    # read file and evaluate pronounciation
    file_bytes = await file.read()
    audio_file = io.BytesIO(file_bytes)
    result = evaluate(audio_file, word)
    
    # encode audio bytes to base64 string
    audio_base64 = base64.b64encode(file_bytes).decode('utf-8')
    audio_data_url = f"data:audio/mp3;base64,{audio_base64}"
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "word": word,
        "result": result,
        "audio_data_url": audio_data_url
    })

# api endpoint to get a random word in difficulty
@app.get("/api/word", response_class=PlainTextResponse)
async def get_word(difficulty: str):
    return get_random_word_by_difficulty(difficulty)