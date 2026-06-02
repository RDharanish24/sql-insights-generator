# SQL Insights Generator

A local SQL insights app that converts natural-language questions into Snowflake SQL queries and displays results through a React frontend.

## Project structure

- `backend/` - FastAPI service that generates Snowflake SQL using a local Ollama model and executes it.
- `frontend/` - Vite + React UI for entering questions and viewing query results.
- `skills/` - Project documentation notes and architecture references.

## Requirements

- Python 3.11+ (or compatible Python 3.x)
- Node.js 18+ / npm
- Snowflake account access
- Local Ollama service running (`ollama serve`)

## Backend setup

1. Open a terminal in `backend/`.
2. Create and activate a virtual environment:
   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
3. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Create a `.env` file in `backend/` with:
   ```env
   SNOWFLAKE_PASSWORD=your_snowflake_password
   ```
5. Confirm the schema file exists in `backend/`:
   - `IPL_SEMANTIC 4_8_2026, 1_30 AM (1).yaml`

## Run the backend

From `backend/`:
```powershell
python main.py
```

The API runs on `http://0.0.0.0:8000` by default.

## Frontend setup

1. Open a terminal in `frontend/`.
2. Install dependencies:
   ```powershell
   npm install
   ```

## Run the frontend

From `frontend/`:
```powershell
npm run dev
```

Then open the local Vite URL shown in the terminal.

## Usage

- Send a POST request to `http://localhost:8000/api/chat` with JSON:
  ```json
  {
    "query": "your natural language question"
  }
  ```
- The backend returns:
  - `generated_sql` - the Snowflake SQL query produced by the model
  - `results` - query result rows as JSON

## Notes

- The backend uses a local Ollama model (`llama3.1`) to generate SQL.
- Ensure `ollama serve` is running before starting the backend.
- The Snowflake connection is configured in `backend/main.py` and expects `SNOWFLAKE_PASSWORD` in the environment.
- Only the exact schema from the YAML file should be used for query generation.

## Helpful commands

- Backend install: `python -m pip install -r backend/requirements.txt`
- Frontend install: `npm install --prefix frontend`
- Frontend dev: `npm run dev --prefix frontend`
- Check backend health: `GET http://localhost:8000/health`
