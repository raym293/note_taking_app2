from fastapi_mcp import FastApiMCP
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import psycopg2
import redis
import uvicorn
from transcribe import transcribe_first_audio
# import shutil

# Load environment variables
load_dotenv()
PASS = os.getenv('PASS')
USER = os.getenv('USER')
DATABASE = os.getenv('DATABASE')
HOST = os.getenv('HOST')


# Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# FastAPI and mcp mounting
app = FastAPI()

#icon
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(os.path.dirname(__file__), 'icon.ico'))
 
class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-store"
        return response

# Serve static files with no caching
app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")

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

@app.get('/')
async def root():
    return RedirectResponse(url="http://127.0.0.1:8000/static/index.html")

# Add necessary attributes to MCP-integrated routes
@app.get("/notes", operation_id="view_all_notes", tags=["MCP"])
async def view_notes():
    cached_notes = redis_client.get("notes")
    if cached_notes:
        print(eval(cached_notes))
        return {"notes": eval(cached_notes)}

    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    curr = conn.cursor()
    curr.execute("SELECT * FROM notetaker;")
    notes = curr.fetchall()
    conn.close()
    print("Here is notes:\n",notes)
    redis_client.set("notes", str(notes))
    return {"notes": notes}

@app.post("/notes", operation_id="create_note", tags=["MCP"])
async def create_note(note: Note):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    curr = conn.cursor()
    curr.execute(
        "INSERT INTO notetaker (title, content) VALUES (%s, %s);",
        (note.title, note.content),
    )
    conn.commit()
    conn.close()
    redis_client.delete("notes")  # clear cache
    return {"message": "Note created successfully"}

@app.delete("/notes/{note_id}", operation_id="delete_note_given_id", tags=["MCP"])
async def delete_note(note_id: int):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    curr = conn.cursor()
    curr.execute("DELETE FROM notetaker WHERE id = %s;", (note_id,))
    conn.commit()
    conn.close()
    redis_client.delete("notes")  # clear cache
    return {"message": "Note deleted successfully"}

@app.put("/notes/{note_id}", operation_id="update_note_title_or_content", tags=["MCP"])
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
    redis_client.delete("notes")  # clear cache
    return {"message": "Note updated successfully"}

@app.post("/transcribe", operation_id="transcribe", tags=["MCP"])
def transcribe_endpoint():
    """
    Transcribe all audio files in the /audio directory, creating a note for each. For each transcription, summarize the transcribed text and update the note's title to be more appropriate based on the content. This endpoint will continue processing until no audio files remain.
    """
    result = transcribe_first_audio()
    if result:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")

        curr = conn.cursor()
        curr.execute(
            "INSERT INTO notetaker (title, content) VALUES (%s, %s);",
            ("Meeting Note", result),
        )
        conn.commit()
        conn.close()
        redis_client.delete("notes")  # clear cache
        return {"message": "Note created successfully"}
    else:
        return {"error": "No audio files found in the audio directory."}

# Mount MCP server after all routes are declared
mcp = FastApiMCP(
    app,
    name="My Notetaking app's server",
    description="This is an endpoint for mcp server",
    include_operations=["view_all_notes", "create_note", "delete_note_given_id", "update_note_title_or_content","transcribe"]
)
mcp.mount()

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)