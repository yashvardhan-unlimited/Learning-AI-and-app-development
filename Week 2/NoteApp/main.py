from pymongo import MongoClient
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# database connection================================================================
client = MongoClient("mongodb://localhost:27017/")

db = client["note_app"]

login_collection = db["login"]

note_collection = db["notes"]
# ===================================================================================



# We defined all the functions for the note app here. ===============================

def check_password(password):
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not any(char.isdigit() for char in password):
        print("Password must contain at least one digit.")
        return False
    if not any(char.isupper() for char in password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not any(char.islower() for char in password):
        print("Password must contain at least one lowercase letter.")
        return False
    return True

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = login_collection.find_one({"username": username, "password": password})
    if user:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")

def register():
    username = input("Enter username: ")
    existing_user = login_collection.find_one({"username": username})
    if existing_user:
        print("Username already exists. Please choose a different username.")
        return

    password = input("Enter password: ")
    is_valid = check_password(password)
    if not is_valid:
        return

    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return
    else:
        login_collection.insert_one({"username": username, "password": password})
        print("Registration successful.")

# def create_note(username):
#     title = input("Enter note title: ")
#     content = input("Enter note content: ")

#     note_collection.insert_one({"title": title, "content": content, "username": username})
#     print("Note created successfully.")

# def read_notes(username):
#     notes = note_collection.find({"username": username})
#     for note in notes:
#         print(f"Title: {note['title']}")
#         print(f"Content: {note['content']}")
#         print("-" * 20)

# def update_note(username):
#     title = input("Enter the title of the note to update: ")
#     new_content = input("Enter the new content: ")

#     result = note_collection.update_one({"title": title, "username": username}, {"$set": {"content": new_content}})
#     if result.modified_count > 0:
#         print("Note updated successfully.")
#     else:
#         print("Note not found.")

# def delete_note(username):
#     title = input("Enter the title of the note to delete: ")

#     result = note_collection.delete_one({"title": title, "username": username})
#     if result.deleted_count > 0:
#         print("Note deleted successfully.")
#     else:
#         print("Note not found.")    

# ===================================================================================



# Actual program starts here=========================================================
# code structure ->
'''
NoteApp
    - main.py
    - static
        - style.css
    - templates
        - index.html    
    '''

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "index.html", 
        context={
            "request": request
        }
    )
 
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

 

while not True:
    print("\n-----------Welcome to the Note App!----------------------------------")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        register()


    elif choice == "2":
        login()

    elif choice == "3":
        print("Exiting the application.")
        break

    else:
        print("Invalid choice. Please try again.")


