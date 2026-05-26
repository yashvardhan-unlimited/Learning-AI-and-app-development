# ============================================================
# main.py — The heart of the Notepad Web Application
# ============================================================
# FastAPI is a modern Python web framework. Think of it like
# a switchboard: requests come in, we route them to the right
# function, do some work, and send a response back.
# ============================================================

import json
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware

# ──────────────────────────────────────────────
# APP SETUP
# ──────────────────────────────────────────────

app = FastAPI(title="Notepad App")

# SessionMiddleware lets us store small pieces of data (like "who is logged in")
# across requests using a signed cookie. The secret_key must be kept private in
# a real app — it signs the cookie so nobody can tamper with it.
app.add_middleware(SessionMiddleware, secret_key="CHANGE_THIS_IN_PRODUCTION_TO_A_LONG_RANDOM_STRING")

# Tell FastAPI where to find static files (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 is a template engine. It lets us write HTML with placeholders like
# {{ username }} that get filled in with real data before being sent to the browser.
templates = Jinja2Templates(directory="templates")

# passlib handles secure password hashing. "bcrypt" is the algorithm — it's
# slow on purpose, which makes brute-force attacks much harder.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ──────────────────────────────────────────────
# FILE PATHS
# ──────────────────────────────────────────────

# Path objects are nicer than raw strings for file locations.
USERS_FILE = Path("data/users.json")
NOTES_FILE = Path("data/notes.json")


# ──────────────────────────────────────────────
# JSON HELPER FUNCTIONS
# ──────────────────────────────────────────────
# We use JSON files instead of a database. These helpers make
# reading and writing safe — they handle empty/corrupt files gracefully.

def read_json(filepath: Path) -> dict:
    """Read a JSON file and return its contents as a Python dict.
    Returns an empty dict if the file is missing or empty."""
    try:
        content = filepath.read_text(encoding="utf-8").strip()
        if not content:               # file exists but is empty
            return {}
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}                     # safe default


def write_json(filepath: Path, data: dict) -> None:
    """Write a Python dict to a JSON file with nice formatting."""
    filepath.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# ──────────────────────────────────────────────
# PASSWORD HELPERS
# ──────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Convert a plain-text password into a secure hash.
    The hash looks like '$2b$12$...' and cannot be reversed."""
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Check if a plain-text password matches a stored hash."""
    return pwd_context.verify(plain, hashed)


# ──────────────────────────────────────────────
# SESSION HELPERS
# ──────────────────────────────────────────────

def get_current_user(request: Request) -> str | None:
    """Return the logged-in username from the session, or None."""
    return request.session.get("username")


def require_login(request: Request):
    """If no user is logged in, redirect them to the login page.
    Call this at the top of any route that needs authentication."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return None  # means "all good, proceed"


# ──────────────────────────────────────────────
# ROUTES — AUTHENTICATION
# ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page: redirect logged-in users to dashboard, others to login."""
    if get_current_user(request):
        return RedirectResponse(url="/dashboard")
    return RedirectResponse(url="/login")


# ── REGISTER ──────────────────────────────────

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Show the registration form."""
    # If already logged in, no need to register again
    if get_current_user(request):
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@app.post("/register", response_class=HTMLResponse)
async def register_submit(
    request: Request,
    username: str = Form(...),        # Form(...) means "required field from the HTML form"
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    """Handle the registration form submission."""
    users = read_json(USERS_FILE)

    # ── Validation ──
    username = username.strip().lower()  # normalise: trim spaces, lowercase

    if len(username) < 3:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username must be at least 3 characters."
        })

    if username in users:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "That username is already taken. Please choose another."
        })

    if len(password) < 6:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Password must be at least 6 characters."
        })

    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Passwords do not match."
        })

    # ── Save new user ──
    users[username] = {
        "password": hash_password(password),  # NEVER store plain text
        "created_at": datetime.now().isoformat()
    }
    write_json(USERS_FILE, users)

    # Auto-login after registration and send to dashboard
    request.session["username"] = username
    request.session["flash"] = "Welcome! Your account has been created."
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


# ── LOGIN ─────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Show the login form."""
    if get_current_user(request):
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    """Handle login form submission."""
    users = read_json(USERS_FILE)
    username = username.strip().lower()

    # Check username exists AND password is correct
    # We use a single vague error message on purpose — never reveal
    # whether the username or the password was wrong (security best practice).
    user = users.get(username)
    if not user or not verify_password(password, user["password"]):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password."
        })

    # Store username in session — this is how we "remember" who's logged in
    request.session["username"] = username
    request.session["flash"] = f"Welcome back, {username}!"
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


# ── LOGOUT ────────────────────────────────────

@app.get("/logout")
async def logout(request: Request):
    """Clear the session and send the user back to login."""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


# ──────────────────────────────────────────────
# ROUTES — DASHBOARD
# ──────────────────────────────────────────────

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, search: str = ""):
    """Main dashboard: show all notes for the logged-in user."""
    redirect = require_login(request)
    if redirect:
        return redirect

    username = get_current_user(request)
    all_notes = read_json(NOTES_FILE)

    # Get only this user's notes (default to empty dict)
    user_notes_dict = all_notes.get(username, {})

    # Convert dict of notes to a sorted list (newest first)
    notes_list = list(user_notes_dict.values())

    # ── Search filter ──
    if search:
        q = search.lower()
        notes_list = [
            n for n in notes_list
            if q in n["title"].lower() or q in n["content"].lower()
        ]

    # Sort by updated_at descending (most recently edited first)
    notes_list.sort(key=lambda n: n["updated_at"], reverse=True)

    # Consume the flash message (show it once, then remove it)
    flash = request.session.pop("flash", None)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": username,
        "notes": notes_list,
        "search": search,
        "flash": flash,
        "note_count": len(user_notes_dict),  # total, unfiltered
    })


# ──────────────────────────────────────────────
# ROUTES — NOTES CRUD
# ──────────────────────────────────────────────

# ── CREATE ────────────────────────────────────

@app.get("/notes/new", response_class=HTMLResponse)
async def new_note_page(request: Request):
    """Show blank note editor for creating a new note."""
    redirect = require_login(request)
    if redirect:
        return redirect

    return templates.TemplateResponse("editor.html", {
        "request": request,
        "note": None,        # None signals "create mode" in the template
        "error": None,
    })


@app.post("/notes/new", response_class=HTMLResponse)
async def new_note_submit(
    request: Request,
    title: str = Form(...),
    content: str = Form(""),   # content is optional — empty note is fine
):
    """Save a brand-new note."""
    redirect = require_login(request)
    if redirect:
        return redirect

    username = get_current_user(request)
    title = title.strip()

    if not title:
        return templates.TemplateResponse("editor.html", {
            "request": request,
            "note": None,
            "error": "Title cannot be empty.",
        })

    all_notes = read_json(NOTES_FILE)

    # Make sure this user has a section in the notes file
    if username not in all_notes:
        all_notes[username] = {}

    now = datetime.now().isoformat()
    note_id = str(uuid.uuid4())   # unique ID so we can find/edit/delete this note

    all_notes[username][note_id] = {
        "id": note_id,
        "title": title,
        "content": content,
        "created_at": now,
        "updated_at": now,
    }

    write_json(NOTES_FILE, all_notes)
    request.session["flash"] = f'Note "{title}" created successfully!'
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


# ── EDIT ──────────────────────────────────────

@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_page(request: Request, note_id: str):
    """Show the editor pre-filled with an existing note."""
    redirect = require_login(request)
    if redirect:
        return redirect

    username = get_current_user(request)
    all_notes = read_json(NOTES_FILE)

    # Security: make sure the note belongs to the logged-in user
    note = all_notes.get(username, {}).get(note_id)
    if not note:
        request.session["flash"] = "Note not found."
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("editor.html", {
        "request": request,
        "note": note,   # non-None signals "edit mode" in the template
        "error": None,
    })


@app.post("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_submit(
    request: Request,
    note_id: str,
    title: str = Form(...),
    content: str = Form(""),
):
    """Save changes to an existing note."""
    redirect = require_login(request)
    if redirect:
        return redirect

    username = get_current_user(request)
    title = title.strip()

    if not title:
        # Re-fetch note to repopulate the form
        all_notes = read_json(NOTES_FILE)
        note = all_notes.get(username, {}).get(note_id, {})
        note["title"] = title
        note["content"] = content
        return templates.TemplateResponse("editor.html", {
            "request": request,
            "note": note,
            "error": "Title cannot be empty.",
        })

    all_notes = read_json(NOTES_FILE)

    # Verify ownership again on POST (never trust the URL alone)
    if username not in all_notes or note_id not in all_notes[username]:
        request.session["flash"] = "Note not found."
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

    # Preserve original created_at; update everything else
    all_notes[username][note_id]["title"] = title
    all_notes[username][note_id]["content"] = content
    all_notes[username][note_id]["updated_at"] = datetime.now().isoformat()

    write_json(NOTES_FILE, all_notes)
    request.session["flash"] = "Note updated."
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


# ── DELETE ────────────────────────────────────

@app.post("/notes/{note_id}/delete")
async def delete_note(request: Request, note_id: str):
    """Permanently delete a note. The confirmation happens via an HTML form."""
    redirect = require_login(request)
    if redirect:
        return redirect

    username = get_current_user(request)
    all_notes = read_json(NOTES_FILE)

    # Security: only delete if it belongs to the current user
    if username in all_notes and note_id in all_notes[username]:
        title = all_notes[username][note_id]["title"]
        del all_notes[username][note_id]
        write_json(NOTES_FILE, all_notes)
        request.session["flash"] = f'Note "{title}" deleted.'

    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
