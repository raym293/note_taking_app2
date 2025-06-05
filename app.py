from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import psycopg2
import redis

# Load environment variables
load_dotenv()
PASS = os.getenv('PASS')
USER = os.getenv('USER')
DATABASE = os.getenv('DATABASE')
HOST = os.getenv('HOST')

# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Initialize FastAPI
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database connection function
def get_connection():
    try:
        return psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASS,
            host=HOST,
            port=5432,
        )
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Pydantic model for notes
class Note(BaseModel):
    id: int
    title: str
    content: str

@app.get("/notes")
async def view_notes():
    """Fetch all notes."""
    cached_notes = redis_client.get("notes")
    if cached_notes:
        return {"notes": eval(cached_notes)}

    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    curr = conn.cursor()
    curr.execute("SELECT * FROM notetaker;")
    notes = curr.fetchall()
    conn.close()

    redis_client.set("notes", str(notes))
    return {"notes": notes}

@app.post("/notes")
async def create_note(note: Note):
    """Create a new note."""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    curr = conn.cursor()
    curr.execute(
        "INSERT INTO notetaker (id, title, content) VALUES (%s, %s, %s);",
        (note.id, note.title, note.content),
    )
    conn.commit()
    conn.close()

    redis_client.delete("notes")  # Invalidate cache
    return {"message": "Note created successfully"}

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    """Delete a note by ID."""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    curr = conn.cursor()
    curr.execute("DELETE FROM notetaker WHERE id = %s;", (note_id,))
    conn.commit()
    conn.close()

    redis_client.delete("notes")  # Invalidate cache
    return {"message": "Note deleted successfully"}

@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: Note):
    """Update a note by ID."""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    curr = conn.cursor()
    curr.execute(
        "UPDATE notetaker SET title = %s, content = %s WHERE id = %s;",
        (note.title, note.content, note_id),
    )
    conn.commit()
    conn.close()

    redis_client.delete("notes")  # Invalidate cache
    return {"message": "Note updated successfully"}