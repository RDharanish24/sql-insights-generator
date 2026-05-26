import os
import yaml
import pandas as pd
import re 
import snowflake.connector
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import ollama  # Local Ollama client integration

# Load environment variables from the local .env file
load_dotenv()

def load_schema(file_path=None):
    """Loads the database schema from the YAML file."""
    if file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "IPL_SEMANTIC 4_8_2026, 1_30 AM (1).yaml")
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[ERROR] Schema file '{file_path}' not found.")
        try:
            parent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "IPL_SEMANTIC 4_8_2026, 1_30 AM (1).yaml")
            with open(parent_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"[ERROR] Schema file also not found in parent: '{parent_path}'")
        return {'database_schema': {'tables': []}}
    
DB_SCHEMA = load_schema()


# --- Prompt Configuration ---
SCHEMA_PROMPT = f"""
You are an expert Snowflake SQL query generator.
Your task is to convert a natural language question into a single, valid, and executable Snowflake SQL query.

DATABASE SCHEMA:
---
{yaml.dump(DB_SCHEMA, indent=2)}
---

CRITICAL SEMANTIC RULES:
1. ONLY use the table names and column names defined in the database schema above. DO NOT invent tables (e.g., do NOT use 'players', 'batsmen', 'bowlers', etc.).
2. Batter stats (runs scored by a batsman):
   - Table: `BALL_BY_BALL`
   - Batter name column: `BATTER`
   - Batter runs column: `BATTER_RUNS`
   - Example to get top 10 batsmen with most runs:
     `SELECT BATTER, SUM(BATTER_RUNS) AS TOTAL_RUNS FROM BALL_BY_BALL GROUP BY BATTER ORDER BY TOTAL_RUNS DESC LIMIT 10`
3. Bowler stats (wickets taken by a bowler):
   - Table: `BALL_BY_BALL`
   - Bowler name column: `BOWLER`
   - Wicket indicator: `IS_WICKET` (BOOLEAN)
   - Wicket method column: `WICKET_KIND` (values like caught, lbw, bowled, etc. Note: 'run out' is not credited to the bowler)
   - Example to get top 5 bowlers with most wickets:
     `SELECT BOWLER, COUNT(*) AS WICKETS FROM BALL_BY_BALL WHERE IS_WICKET = TRUE AND WICKET_KIND != 'run out' GROUP BY BOWLER ORDER BY WICKETS DESC LIMIT 5`
4. Matches won, played, or seasons stats:
   - Table: `IPL_MATCH`
   - Season: `SEASON` (VARCHAR, e.g. '2008') or `SEASON_ID` (NUMBER, e.g. 2008)
   - Winner column: `MATCH_WINNER`
   - Toss winner column: `TOSS_WINNER`
   - Toss decision column: `TOSS_DECISION`
   - Venue column: `VENUE`
5. Joins:
   - If a question asks about player details (like batting style `BAT_STYLE` or bowling style `BOWL_STYLE` from `PLAYER_INFO`) combined with stats:
     Join `BALL_BY_BALL` or `IPL_MATCH` with `PLAYER_INFO` using `PLAYER_INFO.PLAYER_NAME`.

RULES:
1. Only output the raw SQL query. Do not include any explanations, comments, or surrounding text (like '```sql').
2. Ensure the query is syntactically correct for Snowflake SQL.
3. Use the exact uppercase table and column names provided in the schema.
4. Use UNQUALIFIED table names only (e.g., `BALL_BY_BALL`, NOT `DEMO_DB.PUBLIC.BALL_BY_BALL` or `NLP2SQL.TEST_SCHEMA.BALL_BY_BALL`). The database and schema context is already set in the connection.
"""


def execute_sql_query(sql_query):
    """Connects to Snowflake, executes the query, and returns the result."""
    if not sql_query or not sql_query.strip():
        print("\n[ERROR] Generated SQL query is empty.")
        return None, None

    try:
        snowflake_pwd = os.environ.get('SNOWFLAKE_PASSWORD')
        if not snowflake_pwd:
            print("\n[ERROR] SNOWFLAKE_PASSWORD not found in environment variables.")
            return None, None

        print("[INFO] Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user='DHARANISH',
            password=snowflake_pwd,
            account='ndoifsk-lo49799',  
            warehouse='COMPUTE_WH',
            database='NLP2SQL',
            schema='TEST_SCHEMA'
        )
        
        print("[INFO] Connected to Snowflake successfully.")
        cur = conn.cursor()

        print(f"[INFO] Executing SQL query ({len(sql_query)} chars)...")
        cur.execute(sql_query)

        rows = cur.fetchall()
        column_names = [i[0] for i in cur.description] if cur.description else None

        print(f"[INFO] Query execution successful. Fetched {len(rows) if rows else 0} rows.")
        
        conn.close()
        return rows, column_names

    except snowflake.connector.errors.ProgrammingError as pe:
        print(f"\n[ERROR] Snowflake SQL Error (ProgrammingError):")
        print(f"  Code: {pe.errno}")
        print(f"  Message: {pe.msg}")
        return None, None
    except Exception as e:
        print(f"\n[ERROR] Unexpected error during database execution: {str(e)}")
        return None, None


# --- Main Chatbot Logic ---
OLLAMA_MODEL = 'llama3.1'

def chatbot_main(user_query):
    """Generates SQL using local Ollama model, executes it, and returns (sql, rows, columns)."""
    print(f"\n{'='*60}\nUser Query: {user_query}\n{'='*60}\n")

    try:
        print(f"[INFO] Calling local Ollama ({OLLAMA_MODEL}) for SQL generation...")
        full_prompt = f"{SCHEMA_PROMPT}\n\nNatural Language Question: {user_query}\n\nGenerated SQL (return ONLY the pure SQL query string, absolutely no markdown wrappers, conversational explanations, or backticks):"
        
        response = ollama.generate(
            model=OLLAMA_MODEL,
            prompt=full_prompt,
            options={
                'temperature': 0.1,  # Lower temperature means high structure compliance
                'top_p': 0.9,
                'num_predict': 1024
            }
        )

        if not response or 'response' not in response or not response['response']:
            print("[ERROR] Local Ollama model returned an empty response string.")
            return None, None, None

        generated_sql = response['response'].strip()
        print(f"[DEBUG] Raw Ollama Output:\n{generated_sql}\n")

        # Strip Markdown block structures cleanly if returned by the LLM
        generated_sql = re.sub(r'^```sql\s*', '', generated_sql, flags=re.IGNORECASE)
        generated_sql = re.sub(r'^```\s*', '', generated_sql)
        generated_sql = re.sub(r'\s*```$', '', generated_sql)
        generated_sql = generated_sql.strip().strip('`').strip(';')

        if not generated_sql:
            return None, None, None

        # Execute query on Snowflake
        rows, columns = execute_sql_query(generated_sql)
        return generated_sql, rows, columns

    except Exception as e:
        print(f"[ERROR] Chatbot execution encountered an error: {e}")
        return None, None, None


# --- FastAPI Implementation ---
app = FastAPI(title="NLP to Snowflake SQL Chatbot API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    sql, rows, columns = chatbot_main(request.query)
    
    if sql is None:
        raise HTTPException(status_code=500, detail="Failed to process query or execute SQL.")
        
    # Standardize result payloads into a structured array of JSON objects
    results_json = []
    if rows and columns:
        df = pd.DataFrame(rows, columns=columns)
        results_json = df.to_dict(orient="records")

    return {
        "status": "success",
        "query": request.query,
        "generated_sql": sql,
        "results": results_json
    }

@app.get("/health")
async def health_check():
    try:
        ollama.list()
        ollama_status = "connected"
    except Exception:
        ollama_status = "disconnected (make sure 'ollama serve' is active)"
        
    return {
        "status": "healthy",
        "ollama_backend": ollama_status,
        "schema_loaded": len(DB_SCHEMA.get('database_schema', {}).get('tables', [])) > 0
    }

if __name__ == "__main__":
    print("[INFO] Checking Ollama availability...")
    try:
        ollama.list()
        print(f"[INFO] Local Ollama engine verified successfully.")
    except Exception as e:
        print(f"\n[WARNING] Could not communicate with local Ollama service: {e}")
        print("[WARNING] Please make sure Ollama is running (`ollama serve`).")

    uvicorn.run(app, host="0.0.0.0", port=8000)