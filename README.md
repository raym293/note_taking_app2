# Note Taking Application

![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![Version](https://img.shields.io/badge/version-v1.0-orange)
![Chat](https://img.shields.io/badge/chat-active-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-framework-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-blue)
![Redis](https://img.shields.io/badge/Redis-cache-red)
![MCP](https://img.shields.io/badge/MCP-enabled-purple)

## Description
This is a simple note-taking application built with FastAPI for the backend, PostgreSQL for persistent storage, and Redis for caching. The frontend is implemented using HTML, CSS, and JavaScript. The backend also supports Model Context Protocol (MCP) for LLM and tool integration.

## Features
- View, add, edit, and delete notes.
- Persistent storage using PostgreSQL.
- Caching with Redis for faster data retrieval.
- MCP server for LLM and tool integration (via fastapi_mcp).

## Prerequisites
Make sure you have the following installed on your system:
- Python 3.10 or higher
- PostgreSQL
- Redis

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd note_taking_app2
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file:
   Create a `.env` file in the root directory with the following content:
   ```env
   DATABASE="your_database_name"
   USER="your_database_user"
   PASS="your_database_password"
   HOST="127.0.0.1"
   ```

5. Set up the PostgreSQL database:
   - Create a database named `your_database_name`.
   - Run the necessary SQL commands to create the `notetaker` table.

6. Start the Redis server:
   ```bash
   redis-server
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

3. Access the API documentation at:
   ```
   http://127.0.0.1:8000/docs
   ```

4. (Optional) Use MCP tools:
   - Ensure you have the [VS Code MCP extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.mcp) installed.
   - The MCP server will be available at `http://127.0.0.1:8000/mcp`.
   - You can interact with your app using LLMs and tool calls.

## Project Structure
- `app.py`: Backend logic for FastAPI and MCP integration.
- `static/`: Contains frontend files (`index.html`, `styles.css`, `script.js`, `icon.png`).
- `README.md`: Project documentation.
- `.env`: Environment variables for database configuration.
- `requirements.txt`: Python dependencies.

## License
This project is licensed under the MIT License.