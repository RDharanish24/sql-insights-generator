import os
import yaml
import pandas as pd
import re 
from google import genai
from google.genai import types
import snowflake.connector
from dotenv import load_dotenv

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
        # Try parent directory just in case
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
        # Fetching credentials securely from local environment variables
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

        # Execute the query
        print(f"[INFO] Executing SQL query ({len(sql_query)} chars)...")
        cur.execute(sql_query)

        # Get the results and column names
        rows = cur.fetchall()
        column_names = [i[0] for i in cur.description] if cur.description else None

        print(f"[INFO] Query execution successful. Fetched {len(rows) if rows else 0} rows.")
        
        conn.close()
        return rows, column_names

    except snowflake.connector.errors.ProgrammingError as pe:
        print(f"\n[ERROR] Snowflake SQL Error (ProgrammingError):")
        print(f"  Code: {pe.errno}")
        print(f"  Message: {pe.msg}")
        print(f"  SQL State: {pe.sqlstate if hasattr(pe, 'sqlstate') else 'N/A'}")
        return None, None
    except snowflake.connector.errors.DatabaseError as de:
        print(f"\n[ERROR] Snowflake Database Error:")
        print(f"  Message: {str(de)}")
        return None, None
    except Exception as e:
        print(f"\n[ERROR] Unexpected error during database execution:")
        print(f"  Type: {type(e).__name__}")
        print(f"  Message: {str(e)}")
        import traceback
        print(f"  Traceback:\n{traceback.format_exc()}")
        return None, None
    
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Initialize the Gemini Client with local environment variable
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("\n[CRITICAL ERROR] GEMINI_API_KEY not found in environment variables!")
    print("Please set GEMINI_API_KEY in your .env file")
    raise ValueError("[ERROR] GEMINI_API_KEY not found. Please set it in your .env file.")

print(f"[INFO] Initializing Gemini API client...")
try:
    client = genai.Client(api_key=api_key)
    print(f"[INFO] Gemini API client initialized successfully (key length: {len(api_key)} chars)")
except Exception as e:
    print(f"[ERROR] Failed to initialize Gemini client: {e}")
    raise

# --- Main Chatbot Logic ---
def chatbot_main(user_query):
    """Generates SQL using Gemini, executes it, and returns (sql, rows, columns)."""
    print(f"\n{'='*60}")
    print(f"User Query: {user_query}")
    print(f"{'='*60}\n")

    # 1. Generate SQL using Gemini
    try:
        print("[INFO] Calling Gemini API for SQL generation...")
        
        # Build the complete prompt
        full_prompt = f"{SCHEMA_PROMPT}\n\nNatural Language Question: {user_query}\n\nGenerated SQL (return ONLY the SQL query, no explanations):"
        
        # Call Gemini API with proper configuration
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1024
            )
        )

        if not response or not hasattr(response, 'text') or not response.text:
            print("[ERROR] Gemini API returned empty response.")
            print(f"[DEBUG] Response object: {response}")
            return None, None, None

        generated_sql = response.text.strip()
        print(f"[DEBUG] Raw Gemini Output:\n{generated_sql}\n")

        # 2. Strip Markdown/Code wrappers from the SQL
        generated_sql = re.sub(r'^```(?:sql)?[\s\n]*', '', generated_sql, flags=re.IGNORECASE)
        generated_sql = re.sub(r'[\s\n]*```$', '', generated_sql, flags=re.IGNORECASE)
        generated_sql = generated_sql.strip()
        
        print(f"[DEBUG] Cleaned SQL:\n{generated_sql}\n")

        if not generated_sql or generated_sql.lower() == 'sql':
            print("[ERROR] Failed to generate a valid SQL query (empty or invalid after cleaning).")
            return None, None, None

        # Basic SQL validation
        if not any(kw in generated_sql.upper() for kw in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
            print("[ERROR] Generated text doesn't look like valid SQL.")
            print(f"[DEBUG] Generated text: {generated_sql}")
            return None, None, None

    except Exception as e:
        print(f"\n[ERROR] Gemini API call failed with exception:")
        print(f"  Type: {type(e).__name__}")
        print(f"  Message: {str(e)}")
        import traceback
        print(f"  Traceback:\n{traceback.format_exc()}")
        return None, None, None

    # 3. Execute the cleaned SQL
    print(f"[INFO] Executing SQL query...")
    rows, column_names = execute_sql_query(generated_sql)

    if rows is None:
        print(f"[ERROR] SQL execution failed.")
        return generated_sql, None, None

    print(f"[INFO] Query executed successfully. Returned {len(rows)} rows with {len(column_names)} columns.")
    return generated_sql, rows, column_names

# --- FastAPI Server Setup ---
app = FastAPI(title="DataGenie Core API", description="Natural Language to Snowflake BI Engine")

# Add CORS Middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify the actual frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "DataGenie Core API",
        "version": "1.0",
        "schema_loaded": DB_SCHEMA is not None and len(str(DB_SCHEMA)) > 10,
        "gemini_configured": api_key is not None and len(api_key) > 10
    }

class QueryRequest(BaseModel):
    prompt: str

@app.post("/api/query")
async def execute_query(payload: QueryRequest):
    """API endpoint to execute natural language query."""
    if not payload.prompt.strip():
        raise HTTPException(
            status_code=400, 
            detail="Prompt cannot be empty."
        )
    
    try:
        print(f"\n{'='*60}")
        print(f"API Request: {payload.prompt}")
        print(f"{'='*60}\n")
        
        sql, rows, columns = chatbot_main(payload.prompt)
        
        # Check if SQL generation failed
        if sql is None:
            print("\n[ERROR] SQL generation failed - sql is None")
            raise HTTPException(
                status_code=500, 
                detail="⚠️ Failed to translate query to SQL. Please check the query syntax and try again. The Gemini API may have encountered an issue."
            )
        
        # Check if SQL execution failed
        if rows is None or columns is None:
            print(f"\n[ERROR] SQL execution failed - rows: {rows is None}, columns: {columns is None}")
            error_msg = f"Failed to execute query on Snowflake. "
            error_msg += f"Generated SQL:\n\n{sql}\n\n"
            error_msg += "Possible issues:\n"
            error_msg += "• Schema or table names don't exist\n"
            error_msg += "• Column references are incorrect\n"
            error_msg += "• Snowflake connection failed\n"
            error_msg += "• Check database credentials"
            raise HTTPException(status_code=500, detail=error_msg)
            
        # Convert rows into list of dicts for the frontend
        # Snowflake results are often tuples, convert to serializable formats
        data_records = []
        for row in rows:
            record = {}
            for col, val in zip(columns, row):
                # Ensure values are JSON serializable (like decimal, datetime)
                if hasattr(val, 'isoformat'):
                    record[col] = val.isoformat()
                elif hasattr(val, 'to_eng_string'):  # Decimal types
                    record[col] = float(val)
                else:
                    record[col] = val
            data_records.append(record)
        
        print(f"[SUCCESS] Query executed and returned {len(data_records)} records")
        return {
            "sql": sql,
            "data": data_records,
            "columns": columns
        }
        
    except HTTPException as he:
        # Re-raise HTTPExceptions as-is
        raise he
    except Exception as e:
        print(f"\n[ERROR] Unexpected API error:")
        print(f"  Type: {type(e).__name__}")
        print(f"  Message: {str(e)}")
        import traceback
        print(f"  Traceback:\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

# Standard Python entry point for running locally
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 DataGenie Core API Server Starting...")
    print("="*70)
    print(f"📍 Base URL: http://localhost:8000")
    print(f"📊 Query Endpoint: POST http://localhost:8000/api/query")
    print(f"❤️  Health Check: GET http://localhost:8000/health")
    print(f"📖 Docs: http://localhost:8000/docs")
    print(f"\n⚙️  Configuration:")
    print(f"   • Gemini API: {'✅ Configured' if api_key else '❌ NOT Configured'}")
    print(f"   • Schema Loaded: {'✅ Yes' if DB_SCHEMA and len(str(DB_SCHEMA)) > 10 else '❌ No'}")
    print(f"   • Database: NLP2SQL.TEST_SCHEMA")
    print("="*70 + "\n")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
