document.addEventListener("DOMContentLoaded", () => {
    const notesList = document.getElementById("notes-list");
    const addNoteForm = document.getElementById("add-note-form");

    // Fetch notes from the backend
    async function fetchNotes() {
        const response = await fetch("/notes");
        const data = await response.json();
        notesList.innerHTML = "";
        data.notes.forEach(note => {
            const li = document.createElement("li");
            li.innerHTML = `
                <strong>${note[1]}</strong>
                <p>${note[2]}</p>
                <button onclick="deleteNote(${note[0]})">Delete</button>
                <button onclick="editNote(${note[0]}, '${note[1]}', '${note[2]}')">Edit</button>
            `;
            notesList.appendChild(li);
        });
    }

    // Add a new note
    addNoteForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        console.log("Form submitted"); // Debugging log

        const title = document.getElementById("note-title").value;
        const content = document.getElementById("note-content").value;

        console.log("Title:", title); // Debugging log
        console.log("Content:", content); // Debugging log

        await fetch("/notes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: Date.now(), title, content }),
        });

        console.log("POST request sent"); // Debugging log

        fetchNotes();
        addNoteForm.reset();
    });

    // Expose deleteNote to the global scope
    async function deleteNote(noteId) {
        await fetch(`/notes/${noteId}`, {
            method: "DELETE",
        });
        fetchNotes();
    }
    window.deleteNote = deleteNote;

    // Expose editNote to the global scope
    async function editNote(noteId, currentTitle, currentContent) {
        const newTitle = prompt("Edit Title:", currentTitle);
        const newContent = prompt("Edit Content:", currentContent);

        if (newTitle && newContent) {
            await fetch(`/notes/${noteId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ id: noteId, title: newTitle, content: newContent }),
            });
            fetchNotes();
        }
    }
    window.editNote = editNote;

    // Initial fetch
    fetchNotes();
});
