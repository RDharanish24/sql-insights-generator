import os
import yaml
import pandas as pd
import re 
import streamlit as nn  # Imported at the top, but we will use standard streamlit alias below
import streamlit as st
from google import genai
from google.genai import types
import snowflake.connector
from dotenv import load_dotenv

# Set page config at the very top
st.set_page_config(page_title="IPL SQL Insights Generator", page_icon="🏏", layout="wide")

# Load environment variables from the local .env file
load_dotenv()

# --- Cached Data Loading ---
@st.cache_data
def load_schema(file_path=r"C:\Users\DELL\Documents\ml projects\sql insights generator\IPL_SEMANTIC 4_8_2026, 1_30 AM (1).yaml."):
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        st.error(f"Schema file '{file_path}' not found.")
        return {'database_schema': {'tables': []}}

DB_SCHEMA = load_schema()

# --- Updated Prompt Configuration to target Snowflake ---
SCHEMA_PROMPT = f"""
You are an expert Snowflake SQL query generator.
Your task is to convert a natural language question into a single, valid, and executable Snowflake SQL query.

DATABASE SCHEMA:
---
{yaml.dump(DB_SCHEMA, indent=2)}
---

RULES:
1. Only output the SQL query. Do not include any explanations, comments, or surrounding text (like '```sql').
2. Ensure the query is syntactically correct for Snowflake SQL.
3. Use the exact table and column names provided in the schema.
"""

def execute_sql_query(sql_query):
    """Connects to Snowflake, executes the query, and returns the result."""
    if not sql_query:
        return None, None, "Generated SQL query is empty."

    try:
        snowflake_pwd = os.environ.get('SNOWFLAKE_PASSWORD')
        if not snowflake_pwd:
            return None, None, "SNOWFLAKE_PASSWORD not found in environment variables."

        conn = snowflake.connector.connect(
            user='DHARANISH',
            password=snowflake_pwd,
            account='ndoifsk-lo49799',  
            warehouse='COMPUTE_WH',
            database='NLP2SQL',
            schema='TEST_SCHEMA'
        )
        cur = conn.cursor()
        cur.execute(sql_query)

        rows = cur.fetchall()
        column_names = [i[0] for i in cur.description] if cur.description else None

        conn.close()
        return rows, column_names, None

    except Exception as e:
        return None, None, str(e)

# Initialize the Gemini Client
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- Streamlit UI Layout ---
st.title("🏏 IPL SQL Insights Generator")
st.markdown("Ask questions about IPL data in plain English, and watch Gemini build and run the Snowflake SQL queries live!")

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "df" in message:
            st.dataframe(message["df"])
        if "sql" in message:
            with st.expander("View Generated SQL"):
                st.code(message["sql"], language="sql")

# React to user input
if user_query := st.chat_input("e.g., Which team won the most matches in 2023?"):
    
    # 1. Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Add user message to session history
    new_message_state = {"role": "user", "content": user_query}

    # 2. Generate response inside assistant container
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        with st.spinner("AI is translating your question to SQL..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        SCHEMA_PROMPT,
                        f"Natural Language Question: {user_query}\n\nGenerated SQL:"
                    ],
                    config=types.GenerateContentConfig(temperature=0.4)
                )
                generated_sql = response.text.strip()
                # Clean up wrapping markers
                generated_sql = re.sub(r'```sql\s*|\s*```', '', generated_sql, flags=re.IGNORECASE).strip()
            except Exception as e:
                st.error(f"Gemini API call failed: {e}")
                st.stop()

        if generated_sql:
            # Show the generated SQL in an expander toggle
            with st.expander("⚡ View Generated SQL", expanded=True):
                st.code(generated_sql, language="sql")
            new_message_state["sql"] = generated_sql
            
            # 3. Execute the SQL query
            with st.spinner("Executing query on Snowflake..."):
                rows, column_names, error_msg = execute_sql_query(generated_sql)

            if error_msg:
                st.error(f"Snowflake Error: {error_msg}")
                new_message_state["content"] = f"❌ Execution failed with error: {error_msg}"
            elif rows and column_names:
                df = pd.DataFrame(rows, columns=column_names)
                st.success("Query Executed Successfully!")
                st.dataframe(df, use_container_width=True)
                
                new_message_state["content"] = "Here are the insights I pulled from the database:"
                new_message_state["df"] = df
            elif rows is not None:
                st.info("Query executed successfully, but returned 0 rows.")
                new_message_state["content"] = "✅ Query executed successfully. No data matched your request."
            else:
                st.error("Something went wrong while collecting database results.")
                new_message_state["content"] = "❌ Could not retrieve data."
        else:
            st.error("Gemini failed to generate a query framework.")
            new_message_state["content"] = "❌ Failed to generate a valid SQL query framework."

        # Append final interaction package to session memory
        st.session_state.messages.append(new_message_state)