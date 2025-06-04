from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
from backend.evaluator import evaluate
import io

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    words = ["Banana", "Apple", "Orange", "Grape", "Kiwi"]
    word = random.choice(words)
    return templates.TemplateResponse("index.html", {"request": request, "word": word})

# form post handler
@app.post("/upload", response_class=HTMLResponse)
async def post_form(request: Request, word: str = Form(...), file: UploadFile = File(...)):
    # parse file and evaluate pronounciation
    file_bytes = await file.read()
    audio_file = io.BytesIO(file_bytes)
    result = evaluate(audio_file, word)
    
    return templates.TemplateResponse("index.html", {"request": request, "word": word, "result": result})
