from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import random
from evaluator import evaluate

app = FastAPI()
templates = Jinja2Templates(directory="../frontend")

# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    words = ["banana", "apple", "orange", "grape", "kiwi"]
    word = random.choice(words)
    return templates.TemplateResponse("index.html", {"request": request, "word": word})