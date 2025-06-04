import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
from backend.evaluator import evaluate

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    words = ["Banana", "Apple", "Orange", "Grape", "Kiwi"]
    word = random.choice(words)
    return templates.TemplateResponse("index.html", {"request": request, "word": word})

# form post handler
@app.post("/upload", response_class=HTMLResponse)
async def post_form(request: Request, word: str = Form(...), file: UploadFile = File(...)):
    # Save uploaded file
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Evaluate pronunciation using the submitted word
    result = evaluate(filepath, word)

    return templates.TemplateResponse("index.html", {"request": request, "word": word, "result": result})
