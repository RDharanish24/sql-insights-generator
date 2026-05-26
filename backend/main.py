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

def load_schema(file_path=r"C:\Users\DELL\Documents\ml projects\sql insights generator\IPL_SEMANTIC 4_8_2026, 1_30 AM (1).yaml"):
    """Loads the database schema from the YAML file."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[ERROR] Schema file '{file_path}' not found.")
        # Provide a minimal structure to avoid crashing if the file is missing
        return {'database_schema': {'tables': []}}
    
DB_SCHEMA = load_schema()

# --- Prompt Configuration ---
SCHEMA_PROMPT = f"""
You are an expert MySQL query generator.
Your task is to convert a natural language question into a single, valid, and executable MySQL query.

DATABASE SCHEMA:
---
{yaml.dump(DB_SCHEMA, indent=2)}
---

RULES:
1. Only output the SQL query. Do not include any explanations, comments, or surrounding text (like '```sql').
2. Ensure the query is syntactically correct for MySQL.
3. Use the exact table and column names provided in the schema.
"""

def execute_sql_query(sql_query):
    """Connects to Snowflake, executes the query, and returns the result."""
    if not sql_query:
        print("\n[ERROR] Generated SQL query is empty after cleaning.")
        return None, None

    try:
        # Fetching credentials securely from local environment variables
        snowflake_pwd = os.environ.get('SNOWFLAKE_PASSWORD')
        if not snowflake_pwd:
            print("\n[ERROR] SNOWFLAKE_PASSWORD not found in environment variables.")
            return None, None

        conn = snowflake.connector.connect(
            user='DHARANISH',
            password=snowflake_pwd,
            account='ndoifsk-lo49799',  
            warehouse='COMPUTE_WH',
            database='NLP2SQL',
            schema='TEST_SCHEMA'
        )
        cur = conn.cursor()

        # Execute the query
        print(f"\n[INFO] Executing Clean SQL: {sql_query}")
        cur.execute(sql_query)

        # Get the results and column names
        rows = cur.fetchall()
        column_names = [i[0] for i in cur.description] if cur.description else None

        conn.close()
        return rows, column_names

    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred during database execution: {e}")
        return None, None
    
# Initialize the Gemini Client with local environment variable
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError("[ERROR] GEMINI_API_KEY not found. Please set it in your .env file.")

client = genai.Client(api_key=api_key)

# --- Main Chatbot Logic ---
def chatbot_main(user_query):
    """Generates SQL using Gemini, executes it, and displays the result."""
    print(f"User Query: {user_query}")

    # 1. Generate SQL using Gemini
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                SCHEMA_PROMPT,
                f"Natural Language Question: {user_query}\n\nGenerated SQL:"
            ],
            config=types.GenerateContentConfig(
                temperature=0.4
            )
        )

        generated_sql = response.text.strip()

        # 2. Strip Markdown/Code wrappers from the SQL
        generated_sql = re.sub(r'```sql\s*|\s*```', '', generated_sql, flags=re.IGNORECASE).strip()
        print(f"[DEBUG] Raw Gemini Output: {generated_sql}")

        if not generated_sql:
            print("[ERROR] Failed to generate a valid, clean SQL query.")
            return None

    except Exception as e:
        print(f"[ERROR] Gemini API call failed: {e}")
        return None

    # 3. Execute the cleaned SQL
    rows, column_names = execute_sql_query(generated_sql)

    # 4. Display the result as a table
    if rows and column_names:
        print("\n✨ Chatbot Result Table ✨")
        df = pd.DataFrame(rows, columns=column_names)
        print(df.to_markdown(index=False))
        return df
    elif rows is not None:
        print("\n✅ Query executed successfully. No data to display.")
        return None
    else:
        print("\n❌ Could not retrieve or display data due to a prior error.")
        return None

# Standard Python entry point for running locally
if __name__ == "__main__":
    query = "most runs" 

    res = chatbot_main(query)