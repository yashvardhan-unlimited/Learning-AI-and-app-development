# main.py
# A simple notepad web app built with FastAPI.
# Passwords are stored as plain text — fine for learning, not for real apps.

import json
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# ── App setup ──────────────────────────────────────────────────────────────────

app = FastAPI()

# Sessions let us remember who is logged in across requests.
# The secret_key is used to sign the cookie so it can't be tampered with.
app.add_middleware(SessionMiddleware, secret_key="learning-project-secret")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ── File paths ─────────────────────────────────────────────────────────────────

USERS_FILE = Path("data/users.json")
NOTES_FILE = Path("data/notes.json")

# ── JSON helpers ───────────────────────────────────────────────────────────────

def read_json(path):
    """Read a JSON file. Returns {} if the file is empty or missing."""
    try:
        text = path.read_text()
        return json.loads(text) if text.strip() else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_json(path, data):
    """Write a dict to a JSON file."""
    path.write_text(json.dumps(data, indent=2))

# ── Auth helpers ───────────────────────────────────────────────────────────────

def current_user(request):
    """Return the logged-in username, or None."""
    return request.session.get("username")

# ── Routes: auth ───────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if current_user(request):
        return RedirectResponse("/dashboard")
    return RedirectResponse("/login")


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    users = read_json(USERS_FILE)

    if username in users:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username already exists."
        })

    # Storing plain-text password — simple but not secure.
    # In a real app you would hash this with bcrypt.
    users[username] = {"password": password}
    write_json(USERS_FILE, users)

    request.session["username"] = username
    return RedirectResponse("/dashboard", status_code=302)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    users = read_json(USERS_FILE)

    if username not in users or users[username]["password"] != password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Wrong username or password."
        })

    request.session["username"] = username
    return RedirectResponse("/dashboard", status_code=302)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

# ── Routes: notes ──────────────────────────────────────────────────────────────

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login")

    all_notes = read_json(NOTES_FILE)
    # Get only this user's notes, sorted newest first
    notes = sorted(
        all_notes.get(user, {}).values(),
        key=lambda n: n["created_at"],
        reverse=True
    )
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": user,
        "notes": notes
    })


@app.get("/notes/new", response_class=HTMLResponse)
async def new_note_page(request: Request):
    if not current_user(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("editor.html", {"request": request, "note": None, "error": None})

@app.post("/notes/new", response_class=HTMLResponse)
async def new_note(request: Request, title: str = Form(...), content: str = Form("")):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login")

    if not title.strip():
        return templates.TemplateResponse("editor.html", {
            "request": request, "note": None, "error": "Title can't be empty."
        })

    all_notes = read_json(NOTES_FILE)
    if user not in all_notes:
        all_notes[user] = {}

    note_id = str(uuid.uuid4())
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    all_notes[user][note_id] = {
        "id": note_id,
        "title": title,
        "content": content,
        "created_at": now
    }
    write_json(NOTES_FILE, all_notes)
    return RedirectResponse("/dashboard", status_code=302)


@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_page(request: Request, note_id: str):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login")

    all_notes = read_json(NOTES_FILE)
    note = all_notes.get(user, {}).get(note_id)
    if not note:
        return RedirectResponse("/dashboard")

    return templates.TemplateResponse("editor.html", {"request": request, "note": note, "error": None})

@app.post("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note(request: Request, note_id: str, title: str = Form(...), content: str = Form("")):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login")

    all_notes = read_json(NOTES_FILE)
    if user not in all_notes or note_id not in all_notes[user]:
        return RedirectResponse("/dashboard")

    all_notes[user][note_id]["title"] = title
    all_notes[user][note_id]["content"] = content
    write_json(NOTES_FILE, all_notes)
    return RedirectResponse("/dashboard", status_code=302)


@app.post("/notes/{note_id}/delete")
async def delete_note(request: Request, note_id: str):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login")

    all_notes = read_json(NOTES_FILE)
    if user in all_notes and note_id in all_notes[user]:
        del all_notes[user][note_id]
        write_json(NOTES_FILE, all_notes)

    return RedirectResponse("/dashboard", status_code=302)
