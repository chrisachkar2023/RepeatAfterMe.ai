from fastapi import FastAPI, Request, Form, UploadFile, File, Response, status
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
import random
import io
import base64
from passlib.context import CryptContext
from itsdangerous import URLSafeSerializer
from gtts import gTTS
from backend.evaluator import evaluate
from backend.add_user import add_user
from backend.database import SessionLocal, User, Word

# setup FastAPI app
app = FastAPI()
upload_results_cache = {}
user_history_cache = {}

# for frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

SECRET_KEY = "super-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_username_from_cookie(request: Request):
    cookie = request.cookies.get("session")
    if cookie:
        try:
            username = serializer.loads(cookie)
            return username
        except Exception:
            return None
    return None

def get_random_word_by_difficulty(difficulty: str):
    session = SessionLocal()
    words = session.query(Word).filter(Word.difficulty == difficulty.lower()).all()
    session.close()
    if not words:
        return None
    return random.choice([w.word for w in words])


# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    difficulty = request.query_params.get("difficulty") or request.cookies.get("difficulty") or "easy"
    word = get_random_word_by_difficulty(difficulty)
    username = get_username_from_cookie(request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": username,
        "word": word,
        "difficulty": difficulty
    })
    
@app.post("/upload")
async def upload_post(request: Request, word: str = Form(...), difficulty: str = Form(...), file: UploadFile = File(...)):
    file_bytes = await file.read()
    audio_file = io.BytesIO(file_bytes)
    result = evaluate(audio_file, word)
    audio_base64 = base64.b64encode(file_bytes).decode('utf-8')
    audio_data_url = f"data:audio/mp3;base64,{audio_base64}"

    tts = gTTS(text=word, lang='en')
    tts_fp = io.BytesIO()
    tts.write_to_fp(tts_fp)
    tts_fp.seek(0)
    tts_audio_base64 = base64.b64encode(tts_fp.read()).decode('utf-8')
    tts_audio_data_url = f"data:audio/mpeg;base64,{tts_audio_base64}"

    username = get_username_from_cookie(request)


    if username:
        history = user_history_cache.get(username, [])
        history.append({
            "word": word,
            "score": result.get("score") if isinstance(result, dict) else result
        })
        user_history_cache[username] = history[-20:]

    import uuid
    session_id = str(uuid.uuid4())
    upload_results_cache[session_id] = {
        "username": username,
        "word": word,
        "result": result,
        "audio_data_url": audio_data_url,
        "tts_audio_data_url": tts_audio_data_url,
        "difficulty": difficulty
    }

    return RedirectResponse(url=f"/results/{session_id}", status_code=303)

@app.get("/results/{session_id}", response_class=HTMLResponse)
async def show_results(request: Request, session_id: str):
    data = upload_results_cache.get(session_id)
    if not data:
        # if no data found: error 404
        return templates.TemplateResponse("404.html", 
                                      {"request": request},
                                      status_code=404)
    # return regular results if data was found
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": data["username"],
        "word": data["word"],
        "result": data["result"],
        "audio_data_url": data["audio_data_url"],
        "tts_audio_data_url": data["tts_audio_data_url"],
        "difficulty": data["difficulty"]
    })


# API endpoint to get a random word by difficulty
@app.get("/api/word", response_class=PlainTextResponse)
async def get_word(difficulty: str):
    return get_random_word_by_difficulty(difficulty)

# Login page GET
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    # prevents already logged in users from accessing
    username = get_username_from_cookie(request)
    if username:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

# Login form POST
@app.post("/login")
async def login_post(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):    
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()

    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    stored_hash = user.password_hash

    if not pwd_context.verify(password, stored_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    # Create a signed cookie
    session_cookie = serializer.dumps(username)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="session", value=session_cookie, httponly=True)

    return response

# logout route
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="session")
    return response

# sign up page GET
@app.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    # prevents already logged in users from accessing
    username = get_username_from_cookie(request)
    if username:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("signup.html", {"request": request})

# sign up page POST
@app.post("/signup")
async def signup_post(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    # checks if password was entered correctly twice
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Passwords do not match"
        })
    
    # tries to add user to db
    success = add_user(username, password)
    if not success:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Username already exists"
        })

    session_cookie = serializer.dumps(username)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="session", value=session_cookie, httponly=True)
    return response


@app.get("/history", response_class=HTMLResponse)
async def word_history(request: Request):
    username = get_username_from_cookie(request)
    if not username or username not in user_history_cache:
        return HTMLResponse("<p>No history available.</p>", status_code=200)

    history_html = "<ol>"
    for entry in reversed(user_history_cache[username]):
        history_html += f"<li>{entry['word']} - Score: {entry['score']}</li>"
    history_html += "</ol>"
    return HTMLResponse(history_html)


# displays current users
@app.get("/test-users")
def test_users():
    session = SessionLocal()
    users = session.query(User.username).all()
    session.close()
    return {"users": [u[0] for u in users]}


# error 404 handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # custom handler
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        username = get_username_from_cookie(request)
        return templates.TemplateResponse("404.html", {
                            "request": request,
                            "username": username
                            }, status_code=404)
    # default handler
    else:
        return await http_exception_handler(request, exc)