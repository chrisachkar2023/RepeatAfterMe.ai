from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
from evaluator import evaluate

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    words = ["Banana", "Apple", "Orange", "Grape", "Kiwi"]
    word = random.choice(words)
    return templates.TemplateResponse("index.html", {"request": request, "word": word})