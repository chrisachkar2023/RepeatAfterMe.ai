from fastapi import FastAPI, Request, Form, UploadFile, File, Response
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random
import io
import sqlite3
import base64
from fastapi_login import LoginManager
from backend.evaluator import evaluate

app = FastAPI()

# for static frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

# Dummy user database
DB_USERS = {
    "admin": {"username": "admin", "password": "password"}
}

manager = LoginManager("your-secret-key", token_url="/login", use_cookie=True)
manager.cookie_name = "auth_token"

@manager.user_loader
def load_user(username: str):
    return DB_USERS.get(username)

# Returns a random word from a desired difficulty
def get_random_word_by_difficulty(difficulty: str):
    connect = sqlite3.connect("backend/words.db")
    cursor = connect.cursor()
    cursor.execute("SELECT word FROM words WHERE difficulty = ?", (difficulty.lower(),))
    words = [row[0] for row in cursor.fetchall()]
    connect.close()
    return random.choice(words)

# Root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    word = get_random_word_by_difficulty("easy")
    return templates.TemplateResponse("index.html", {"request": request, "word": word})

# Form post handler
@app.post("/upload", response_class=HTMLResponse)
async def post_form(request: Request, word: str = Form(...), file: UploadFile = File(...)):
    file_bytes = await file.read()
    audio_file = io.BytesIO(file_bytes)
    result = evaluate(audio_file, word)
    audio_base64 = base64.b64encode(file_bytes).decode('utf-8')
    audio_data_url = f"data:audio/mp3;base64,{audio_base64}"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "word": word,
        "result": result,
        "audio_data_url": audio_data_url
    })

# API endpoint to get a random word by difficulty
@app.get("/api/word", response_class=PlainTextResponse)
async def get_word(difficulty: str):
    return get_random_word_by_difficulty(difficulty)

# Login page GET
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

# Login form POST
@app.post("/login")
async def login_post(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    user = DB_USERS.get(username)
    if not user or user["password"] != password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"},
            status_code=401
        )
    access_token = manager.create_access_token(data={"sub": username})
    manager.set_cookie(response, access_token)
    # Must return the Response object to send cookie and redirect
    return RedirectResponse(url="/", status_code=302)

# Main page after login (can customize as needed)
@app.get("/main", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "word": get_random_word_by_difficulty("easy")})
