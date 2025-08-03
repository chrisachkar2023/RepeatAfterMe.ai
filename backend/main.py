from fastapi import FastAPI, Request, Form, UploadFile, File, Response, status, Body, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
import random
import io
import base64
import uuid
from passlib.context import CryptContext
from itsdangerous import URLSafeSerializer
from gtts import gTTS
from backend.evaluator import evaluate
from backend.add_user import add_user
from backend.database import SessionLocal, User, Word, SavedWord

# setup FastAPI app
app = FastAPI()
upload_results_cache = {}
user_history_cache = {}
saved_words_cache = {}

# for frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

SECRET_KEY = "super-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# helper function to get username from cookie
def get_username_from_cookie(request: Request):
    cookie = request.cookies.get("session")
    if cookie:
        try:
            username = serializer.loads(cookie)
            return username
        except Exception:
            return None
    return None

# helper function to randomly select a word from some difficulty
def get_random_word_by_difficulty(difficulty: str):
    session = SessionLocal()
    words = session.query(Word).filter(Word.difficulty == difficulty.lower()).all()
    session.close()
    if not words:
        return None
    return random.choice([w.word for w in words])

# helper function to check if word should be starred (if it's a saved word)
def is_word_saved_by_user(username: str, word_text: str) -> bool:
    if not username or not word_text:
        return False
    
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        word_obj = session.query(Word).filter_by(word=word_text).first()
        if not user or not word_obj:
            return False
        
        saved = session.query(SavedWord).filter_by(user_id=user.id, word_id=word_obj.id).first()
        return saved is not None
    finally:
        session.close()


# root (home page)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    difficulty = request.query_params.get("difficulty") or request.cookies.get("difficulty") or "easy"
    word = get_random_word_by_difficulty(difficulty)
    username = get_username_from_cookie(request)
    
    # check for star symbol
    is_saved = is_word_saved_by_user(username, word)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": username,
        "word": word,
        "difficulty": difficulty,
        "is_saved": is_saved
    })
    
@app.post("/upload")
async def upload_post(request: Request, word: str = Form(...), difficulty: str = Form(...), file: UploadFile = File(...)):
    username = get_username_from_cookie(request)
    logged_in = username is not None
    
    file_bytes = await file.read()
    audio_file = io.BytesIO(file_bytes)
    result = evaluate(audio_file, word, logged_in)
    audio_base64 = base64.b64encode(file_bytes).decode('utf-8')
    audio_data_url = f"data:audio/mp3;base64,{audio_base64}"

    tts = gTTS(text=word, lang='en')
    tts_fp = io.BytesIO()
    tts.write_to_fp(tts_fp)
    tts_fp.seek(0)
    tts_audio_base64 = base64.b64encode(tts_fp.read()).decode('utf-8')
    tts_audio_data_url = f"data:audio/mpeg;base64,{tts_audio_base64}"

    if username:
        history = user_history_cache.get(username, [])
        history.append({
            "word": word,
            "score": result.get("score") if isinstance(result, dict) else result
        })
        user_history_cache[username] = history[-20:]

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
    username = get_username_from_cookie(request)
    
    # if no data found: error 404
    if not data:
        return templates.TemplateResponse("404.html", 
                                      {"request": request,
                                       "username": username},
                                      status_code=404)
        
    # checks for star symbol
    word = data["word"]
    is_saved = is_word_saved_by_user(username, word)
    
    # return regular results if data was found
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": data["username"],
        "word": data["word"],
        "result": data["result"],
        "audio_data_url": data["audio_data_url"],
        "tts_audio_data_url": data["tts_audio_data_url"],
        "difficulty": data["difficulty"],
        "is_saved": is_saved
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

# word history sidebar
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


@app.get("/saved", response_class=HTMLResponse)
async def saved_words(request: Request):
    username = get_username_from_cookie(request)
    if not username:
        return HTMLResponse("<p>No Saved Words available.</p>", status_code=200)

    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return HTMLResponse("<p>No Saved Words available.</p>", status_code=200)

        saved = (
            session.query(Word.word)
            .join(SavedWord, Word.id == SavedWord.word_id)
            .filter(SavedWord.user_id == user.id)
            .all()
        )
        saved_words_list = [w.word for w in saved]

        if not saved_words_list:
            return HTMLResponse("<p>No Saved Words available.</p>", status_code=200)

        saved_html = "<ol>"
        for word in sorted(saved_words_list):
            saved_html += f'<li><a href="/practice/{word}">{word}</a></li>'
        saved_html += "</ol>"

        return HTMLResponse(saved_html)

    finally:
        session.close()

@app.post("/api/save-word")
async def save_word(request: Request, data: dict = Body(...)):
    word_text = data.get("word")
    username = get_username_from_cookie(request)
    
    if not username or not word_text:
        return {"success": False}
    
    session = SessionLocal()
    
    try:
        # Get user and word objects
        user = session.query(User).filter_by(username=username).first()
        word_obj = session.query(Word).filter_by(word=word_text).first()

        if not user or not word_obj:
            return {"success": False}

        # Check if already saved
        existing = session.query(SavedWord).filter_by(user_id=user.id, word_id=word_obj.id).first()

        if existing:
            # Word is already saved, so delete it (unsave)
            session.delete(existing)
            session.commit()
            return {"success": True, "saved": False}  # indicates word was removed
        else:
            # Word not saved yet, so add it
            new_saved = SavedWord(user_id=user.id, word_id=word_obj.id)
            session.add(new_saved)
            session.commit()
            return {"success": True, "saved": True}   # indicates word was added
    finally:
        session.close()
        
        
# specifically checks if a word should be starred
@app.get("/api/is-word-saved")
async def is_word_saved(request: Request, word: str = Query(...)):
    username = get_username_from_cookie(request)
    saved = is_word_saved_by_user(username, word)
    return JSONResponse(content={"saved": saved})
    

# saved word links
@app.get("/practice/{word}", response_class=HTMLResponse)
async def practice_word(request: Request, word: str):
    username = get_username_from_cookie(request)
    if not username:
        return RedirectResponse("/login", status_code=302)
    
    session = SessionLocal()
    try:
        word_obj = session.query(Word).filter_by(word=word).first()
        if not word_obj:
            return templates.TemplateResponse("404.html", {
                            "request": request,
                            "username": username
                            }, status_code=404)

        # checks for star symbol
        is_saved = is_word_saved_by_user(username, word)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "username": username,
            "word": word_obj.word,
            "difficulty": word_obj.difficulty,
            "is_saved": is_saved
        })
    finally:
        session.close()
    
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