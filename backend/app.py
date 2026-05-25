import sqlite3
import os
from typing import TypedDict, List, Dict
from google import genai
from google.genai import types
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.types import RetryPolicy

# Load environment variables
load_dotenv()

# --- 1. Configuration & DB Setup ---
# Initialize the modern SDK client globally
client = genai.Client()

def setup_database(db_name="ecommerce.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS users;

        CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT, signup_date DATE, country TEXT);
        CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price DECIMAL(10, 2));
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, 
            order_date DATE, quantity INTEGER, total_amount DECIMAL(10, 2),
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );

        -- 15 Users across 6 countries
        INSERT INTO users VALUES (1, 'Alice Johnson', '2023-01-15', 'USA');
        INSERT INTO users VALUES (2, 'Bob Smith', '2023-01-22', 'UK');
        INSERT INTO users VALUES (3, 'Carlos Rivera', '2023-02-10', 'USA');
        INSERT INTO users VALUES (4, 'Diana Mueller', '2023-02-28', 'Germany');
        INSERT INTO users VALUES (5, 'Eshaan Patel', '2023-03-05', 'India');
        INSERT INTO users VALUES (6, 'Fiona Clarke', '2023-03-18', 'UK');
        INSERT INTO users VALUES (7, 'George Wang', '2023-04-02', 'Canada');
        INSERT INTO users VALUES (8, 'Hannah Kim', '2023-04-15', 'USA');
        INSERT INTO users VALUES (9, 'Ivan Novak', '2023-05-01', 'Germany');
        INSERT INTO users VALUES (10, 'Julia Santos', '2023-05-20', 'Australia');
        INSERT INTO users VALUES (11, 'Kevin Brown', '2023-06-08', 'USA');
        INSERT INTO users VALUES (12, 'Lara Singh', '2023-07-14', 'India');
        INSERT INTO users VALUES (13, 'Marco Rossi', '2023-08-01', 'Canada');
        INSERT INTO users VALUES (14, 'Nina Olsen', '2023-09-12', 'Australia');
        INSERT INTO users VALUES (15, 'Omar Hassan', '2023-10-05', 'UK');

        -- 12 Products across 5 categories
        INSERT INTO products VALUES (101, 'Laptop Pro', 'Electronics', 1500.00);
        INSERT INTO products VALUES (102, 'Wireless Headphones', 'Electronics', 120.00);
        INSERT INTO products VALUES (103, 'Smartphone X', 'Electronics', 950.00);
        INSERT INTO products VALUES (104, 'Coffee Mug Set', 'Home', 25.00);
        INSERT INTO products VALUES (105, 'Desk Lamp', 'Home', 45.00);
        INSERT INTO products VALUES (106, 'Yoga Mat', 'Sports', 35.00);
        INSERT INTO products VALUES (107, 'Running Shoes', 'Sports', 130.00);
        INSERT INTO products VALUES (108, 'Python Programming Book', 'Books', 40.00);
        INSERT INTO products VALUES (109, 'Data Science Handbook', 'Books', 55.00);
        INSERT INTO products VALUES (110, 'Winter Jacket', 'Fashion', 180.00);
        INSERT INTO products VALUES (111, 'Sunglasses', 'Fashion', 75.00);
        INSERT INTO products VALUES (112, 'Fitness Tracker', 'Electronics', 200.00);

        -- 80+ Orders spanning Jan-Dec 2023
        INSERT INTO orders VALUES (1001, 1, 101, '2023-01-18', 1, 1500.00);
        INSERT INTO orders VALUES (1002, 2, 104, '2023-01-20', 2, 50.00);
        INSERT INTO orders VALUES (1003, 1, 102, '2023-01-25', 1, 120.00);
        INSERT INTO orders VALUES (1004, 3, 103, '2023-02-05', 1, 950.00);
        INSERT INTO orders VALUES (1005, 4, 108, '2023-02-12', 3, 120.00);
        INSERT INTO orders VALUES (1006, 5, 106, '2023-02-18', 2, 70.00);
        INSERT INTO orders VALUES (1007, 2, 107, '2023-02-22', 1, 130.00);
        INSERT INTO orders VALUES (1008, 3, 110, '2023-03-01', 1, 180.00);
        INSERT INTO orders VALUES (1009, 6, 102, '2023-03-05', 2, 240.00);
        INSERT INTO orders VALUES (1010, 5, 103, '2023-03-10', 1, 950.00);
        INSERT INTO orders VALUES (1011, 7, 101, '2023-03-15', 1, 1500.00);
        INSERT INTO orders VALUES (1012, 1, 109, '2023-03-20', 1, 55.00);
        INSERT INTO orders VALUES (1013, 8, 111, '2023-04-02', 1, 75.00);
        INSERT INTO orders VALUES (1014, 4, 101, '2023-04-08', 1, 1500.00);
        INSERT INTO orders VALUES (1015, 6, 105, '2023-04-12', 2, 90.00);
        INSERT INTO orders VALUES (1016, 9, 112, '2023-04-18', 1, 200.00);
        INSERT INTO orders VALUES (1017, 3, 107, '2023-04-22', 2, 260.00);
        INSERT INTO orders VALUES (1018, 10, 106, '2023-05-01', 1, 35.00);
        INSERT INTO orders VALUES (1019, 7, 103, '2023-05-05', 1, 950.00);
        INSERT INTO orders VALUES (1020, 5, 108, '2023-05-10', 2, 80.00);
        INSERT INTO orders VALUES (1021, 11, 101, '2023-05-15', 1, 1500.00);
        INSERT INTO orders VALUES (1022, 2, 110, '2023-05-20', 1, 180.00);
        INSERT INTO orders VALUES (1023, 8, 102, '2023-05-25', 1, 120.00);
        INSERT INTO orders VALUES (1024, 12, 104, '2023-06-01', 3, 75.00);
        INSERT INTO orders VALUES (1025, 1, 112, '2023-06-05', 1, 200.00);
        INSERT INTO orders VALUES (1026, 9, 103, '2023-06-10', 1, 950.00);
        INSERT INTO orders VALUES (1027, 11, 107, '2023-06-15', 1, 130.00);
        INSERT INTO orders VALUES (1028, 6, 109, '2023-06-18', 2, 110.00);
        INSERT INTO orders VALUES (1029, 13, 101, '2023-06-22', 1, 1500.00);
        INSERT INTO orders VALUES (1030, 4, 106, '2023-06-28', 2, 70.00);
        INSERT INTO orders VALUES (1031, 10, 111, '2023-07-02', 2, 150.00);
        INSERT INTO orders VALUES (1032, 7, 102, '2023-07-05', 1, 120.00);
        INSERT INTO orders VALUES (1033, 3, 105, '2023-07-10', 1, 45.00);
        INSERT INTO orders VALUES (1034, 12, 103, '2023-07-15', 1, 950.00);
        INSERT INTO orders VALUES (1035, 14, 108, '2023-07-18', 1, 40.00);
        INSERT INTO orders VALUES (1036, 5, 101, '2023-07-22', 1, 1500.00);
        INSERT INTO orders VALUES (1037, 15, 112, '2023-07-28', 1, 200.00);
        INSERT INTO orders VALUES (1038, 8, 107, '2023-08-01', 1, 130.00);
        INSERT INTO orders VALUES (1039, 13, 110, '2023-08-05', 2, 360.00);
        INSERT INTO orders VALUES (1040, 1, 104, '2023-08-10', 4, 100.00);
        INSERT INTO orders VALUES (1041, 11, 103, '2023-08-12', 1, 950.00);
        INSERT INTO orders VALUES (1042, 9, 106, '2023-08-18', 1, 35.00);
        INSERT INTO orders VALUES (1043, 2, 109, '2023-08-22', 1, 55.00);
        INSERT INTO orders VALUES (1044, 14, 101, '2023-08-25', 1, 1500.00);
        INSERT INTO orders VALUES (1045, 6, 112, '2023-08-30', 2, 400.00);
        INSERT INTO orders VALUES (1046, 4, 102, '2023-09-02', 1, 120.00);
        INSERT INTO orders VALUES (1047, 15, 107, '2023-09-05', 1, 130.00);
        INSERT INTO orders VALUES (1048, 10, 105, '2023-09-10', 1, 45.00);
        INSERT INTO orders VALUES (1049, 7, 108, '2023-09-15', 2, 80.00);
        INSERT INTO orders VALUES (1050, 12, 101, '2023-09-18', 1, 1500.00);
        INSERT INTO orders VALUES (1051, 3, 111, '2023-09-22', 1, 75.00);
        INSERT INTO orders VALUES (1052, 13, 103, '2023-09-25', 1, 950.00);
        INSERT INTO orders VALUES (1053, 5, 112, '2023-09-30', 1, 200.00);
        INSERT INTO orders VALUES (1054, 8, 104, '2023-10-02', 2, 50.00);
        INSERT INTO orders VALUES (1055, 11, 110, '2023-10-05', 1, 180.00);
        INSERT INTO orders VALUES (1056, 1, 103, '2023-10-10', 1, 950.00);
        INSERT INTO orders VALUES (1057, 14, 106, '2023-10-12', 3, 105.00);
        INSERT INTO orders VALUES (1058, 9, 107, '2023-10-18', 1, 130.00);
        INSERT INTO orders VALUES (1059, 15, 102, '2023-10-22', 2, 240.00);
        INSERT INTO orders VALUES (1060, 2, 101, '2023-10-25', 1, 1500.00);
        INSERT INTO orders VALUES (1061, 6, 108, '2023-10-30', 1, 40.00);
        INSERT INTO orders VALUES (1062, 7, 112, '2023-11-02', 1, 200.00);
        INSERT INTO orders VALUES (1063, 4, 105, '2023-11-05', 2, 90.00);
        INSERT INTO orders VALUES (1064, 10, 103, '2023-11-08', 1, 950.00);
        INSERT INTO orders VALUES (1065, 12, 107, '2023-11-12', 1, 130.00);
        INSERT INTO orders VALUES (1066, 3, 101, '2023-11-15', 1, 1500.00);
        INSERT INTO orders VALUES (1067, 13, 109, '2023-11-18', 2, 110.00);
        INSERT INTO orders VALUES (1068, 5, 111, '2023-11-22', 1, 75.00);
        INSERT INTO orders VALUES (1069, 8, 106, '2023-11-25', 2, 70.00);
        INSERT INTO orders VALUES (1070, 15, 103, '2023-11-28', 1, 950.00);
        INSERT INTO orders VALUES (1071, 11, 102, '2023-12-01', 2, 240.00);
        INSERT INTO orders VALUES (1072, 1, 107, '2023-12-05', 1, 130.00);
        INSERT INTO orders VALUES (1073, 14, 112, '2023-12-08', 1, 200.00);
        INSERT INTO orders VALUES (1074, 9, 101, '2023-12-10', 1, 1500.00);
        INSERT INTO orders VALUES (1075, 2, 105, '2023-12-12', 1, 45.00);
        INSERT INTO orders VALUES (1076, 6, 103, '2023-12-15', 1, 950.00);
        INSERT INTO orders VALUES (1077, 4, 110, '2023-12-18', 1, 180.00);
        INSERT INTO orders VALUES (1078, 10, 108, '2023-12-20', 2, 80.00);
        INSERT INTO orders VALUES (1079, 7, 111, '2023-12-22', 1, 75.00);
        INSERT INTO orders VALUES (1080, 13, 102, '2023-12-25', 1, 120.00);
        INSERT INTO orders VALUES (1081, 5, 104, '2023-12-28', 2, 50.00);
        INSERT INTO orders VALUES (1082, 12, 106, '2023-12-30', 1, 35.00);
    """)
    return conn

def get_database_schema(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    return "\n".join([row[0] for row in cursor.fetchall() if row[0] is not None])

# --- 2. Upgraded Agent State ---
class AgentState(TypedDict):
    chat_history: List[Dict[str, str]] # Memory for follow-ups
    question: str
    schema: str
    plan: str
    sql_query: str
    data: list
    columns: list
    error: str
    retries: int                       # Tracks correction loops
    analysis: str
    insights: str

# --- 3. Agent Nodes ---

def planner_agent(state: AgentState) -> dict:
    print("-> [Planner Agent] Decomposing user intent...")
    
    # Format memory safely for context
    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in state.get('chat_history', [])])
    
    prompt = f"""
    You are a Lead Data Architect mapping out a data retrieval strategy.
    
    Chat History (Context for follow-up questions):
    {history_str}
    
    Current Question: "{state['question']}"
    Database Schema: {state['schema']}
    
    Task: Decompose the question into a clear, logical step-by-step SQL execution plan.
    
    CRITICAL MEMORY RULE:
    If the current question uses coreferent pronouns like "she", "he", "it", "them", or references a previous topic (e.g., "How much did she spend?"), you MUST look at the Chat History to determine exactly which entity, name, or country the user is talking about. Map that specific entity value directly into your execution plan steps. Do NOT hallucinate placeholder names like 'Jane Doe'.
    
    Do NOT write the SQL. Output only the numbered logical steps.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"plan": response.text.strip()}

def sql_generator_agent(state: AgentState) -> dict:
    print("-> [SQL Generator Agent] Drafting optimized SQL...")
    system_instruction = f"""
    You are an elite SQL Developer. Write highly optimized, valid SQLite queries.
    Schema: {state['schema']}
    Execution Plan: {state['plan']}
    
    Rules:
    1. Only return the raw SQL query. No markdown, no explanations.
    2. CRITICAL: Always select both the target entity (e.g., name, country) AND the numerical metric being calculated (e.g., SUM(total_amount), COUNT(*)) so follow-up agents can analyze the numbers.
    3. Ensure table aliases are used cleanly.
    4. Be mindful of GROUP BY clauses and aggregate functions.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=state['question'],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1
        )
    )
    
    cleaned_sql = response.text.replace("```sql", "").replace("```", "").strip()
    return {"sql_query": cleaned_sql}

def executor_tool(state: AgentState) -> dict:
    print(f"-> [Executor Tool] Attempting to run: {state['sql_query']}")
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    try:
        cursor.execute(state['sql_query'])
        data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        print("   [Executor Tool] Success!")
        return {"data": data, "columns": columns, "error": None}
    except Exception as e:
        print(f"   [Executor Tool] Failed with error: {str(e)}")
        return {"data": [], "columns": [], "error": str(e)}
    finally:
        conn.close()

def sql_validator_agent(state: AgentState) -> dict:
    """Analyzes execution errors and corrects the SQL."""
    current_retries = state.get('retries', 0)
    print(f"-> [Validator Agent] Fixing SQL Error (Attempt {current_retries + 1}/3)...")
    
    prompt = f"""
    You are a Database Administrator debugging a failed SQL query.
    
    Database Schema: {state['schema']}
    Original Request: {state['question']}
    Failed SQL Query: {state['sql_query']}
    Error Message: {state['error']}
    
    Task: Fix the SQL query to resolve the error. 
    Common fixes: Check column names against the schema, fix missing JOIN conditions, or correct syntax.
    Return ONLY the raw, corrected SQL query without markdown or explanation.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1)
    )
    
    cleaned_sql = response.text.replace("```sql", "").replace("```", "").strip()
    return {
        "sql_query": cleaned_sql,
        "retries": current_retries + 1
    }

def analyst_agent(state: AgentState) -> dict:
    if state.get('error') or not state.get('data'):
        return {"analysis": "No valid data to analyze."}
        
    print("-> [Analyst Agent] Identifying trends and anomalies...")
    prompt = f"""
    You are a Senior Data Scientist. 
    Question asked by user: "{state['question']}"
    SQL Query used to get data: {state['sql_query']}
    Data Columns returned: {state['columns']}
    Raw Data returned: {state['data']}
    
    Perform a deep statistical analysis:
    1. Identify highest/lowest values.
    2. If the data contains only a single row, acknowledge that this entity is the top/sole result matching the user's criteria and detail what that value represents quantitatively.
    3. Detect any stark contrasts or anomalies if multiple rows are present.
    Output purely mathematical/statistical observations without business fluff.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"analysis": response.text.strip()}

def insight_generator_agent(state: AgentState) -> dict:
    if state.get('error'):
        return {"insights": f"System Error: Unable to fetch data after {state.get('retries', 0)} attempts. Error: {state['error']}"}
        
    print("-> [Insight Generator] Crafting executive summary...")
    prompt = f"""
    You are a Chief Strategy Officer responding to stakeholders.
    Original Query: {state['question']}
    Statistical Analysis: {state['analysis']}
    
    Task: Translate the statistical findings into actionable business insights.
    - Start with a direct, one-sentence answer to the query.
    - Use bullet points for supporting evidence (trends, anomalies).
    - Conclude with a brief, strategic recommendation based on the data.
    Do NOT mention SQL, raw data structures, or the analysis process.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"insights": response.text.strip()}

# --- 4. LangGraph Setup with Conditional Routing ---

def should_route_to_validator(state: AgentState) -> str:
    """Routing logic after execution."""
    if state.get('error') and state.get('retries', 0) < 3:
        return "sql_validator"
    return "analyst"

def build_graph():
    workflow = StateGraph(AgentState)
    
    # Configure an explicit RetryPolicy object instance
    llm_retry_policy = RetryPolicy(
        max_attempts=3,
        backoff_factor=2.0,  # Wait progressively longer between attempts (e.g., 2s, 4s, 8s)
        retry_on=Exception
    )
    
    # Add nodes with the verified policy object attached
    workflow.add_node("planner", planner_agent, retry=llm_retry_policy)
    workflow.add_node("sql_generator", sql_generator_agent, retry=llm_retry_policy)
    workflow.add_node("executor", executor_tool)
    workflow.add_node("sql_validator", sql_validator_agent, retry=llm_retry_policy)
    workflow.add_node("analyst", analyst_agent, retry=llm_retry_policy)
    workflow.add_node("insight_generator", insight_generator_agent, retry=llm_retry_policy)
    
    # Standard Flow
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "sql_generator")
    workflow.add_edge("sql_generator", "executor")
    
    # Conditional Routing Loop
    workflow.add_conditional_edges(
        "executor",
        should_route_to_validator,
        {
            "sql_validator": "sql_validator",
            "analyst": "analyst"
        }
    )
    
    # Validator goes back to Executor for a retry
    workflow.add_edge("sql_validator", "executor")
    
    # Finish flow
    workflow.add_edge("analyst", "insight_generator")
    workflow.add_edge("insight_generator", END)
    
    return workflow.compile()

# --- 5. Programmatic Query Interface (used by API layer) ---

def run_query(question: str, chat_history: list = None, db_path: str = "ecommerce.db") -> dict:
    """
    Run a user question through the full LangGraph pipeline.
    Returns a dict with all agent outputs: plan, sql_query, data, columns, analysis, insights, retries, error.
    """
    if chat_history is None:
        chat_history = []

    # Ensure DB exists with data
    db_conn = setup_database(db_path)
    schema = get_database_schema(db_conn)
    db_conn.close()

    # Build and run the graph
    graph = build_graph()
    initial_state = {
        "chat_history": chat_history,
        "question": question,
        "schema": schema,
        "plan": "",
        "sql_query": "",
        "data": [],
        "columns": [],
        "error": "",
        "retries": 0,
        "analysis": "",
        "insights": ""
    }

    final_state = graph.invoke(initial_state)

    return {
        "question": question,
        "plan": final_state.get("plan", ""),
        "sql_query": final_state.get("sql_query", ""),
        "columns": final_state.get("columns", []),
        "data": final_state.get("data", []),
        "analysis": final_state.get("analysis", ""),
        "insights": final_state.get("insights", ""),
        "retries": final_state.get("retries", 0),
        "error": final_state.get("error")
    }

# --- 6. CLI Execution Interface ---
if __name__ == "__main__":
    db_conn = setup_database()
    schema = get_database_schema(db_conn)
    db_conn.close()
    
    app = build_graph()
    
    # We maintain memory across loops
    chat_memory = []
    
    print("\n--- Agentic SQL Insight Generator Started ---")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_query = input("\nAsk a business question: ")
        if user_query.lower() in ['exit', 'quit']:
            break
            
        # Initialize state for this specific run
        initial_state = {
            "chat_history": chat_memory,
            "question": user_query,
            "schema": schema,
            "plan": "",
            "sql_query": "",
            "data": [],
            "columns": [],
            "error": "",
            "retries": 0,
            "analysis": "",
            "insights": ""
        }
        
        # Run the graph
        final_state = app.invoke(initial_state)
        
        # Explainability Output (Transparency Layer)
        print("\n" + "="*60)
        print("🔍 EXPLAINABILITY LAYER")
        print("="*60)
        print(f"1. AI Plan:\n{final_state['plan']}\n")
        print(f"2. Generated SQL:\n{final_state['sql_query']}\n")
        if final_state['retries'] > 0:
            print(f"   [!] Query required {final_state['retries']} auto-corrections to execute.\n")
        print(f"3. Raw Data Extracted: {final_state['data']}\n")
        print(f"4. Statistical Analysis:\n{final_state['analysis']}\n")
        
        # Final Business Output
        print("="*60)
        print("🎯 FINAL BUSINESS INSIGHTS")
        print("="*60)
        print(final_state['insights'])
        print("="*60)
        
        # Save to memory for the next follow-up question
        chat_memory.append({"role": "user", "content": user_query})
        chat_memory.append({"role": "assistant", "content": final_state['insights']})