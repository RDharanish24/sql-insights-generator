# 🔧 DataGenie Core - Troubleshooting Guide

## Error: "Query Execution Failed - Failed to translate query to SQL"

This error indicates that the backend cannot translate your natural language query into SQL using the Gemini API. Here's how to diagnose and fix it:

---

## 🚀 Quick Diagnosis

### Step 1: Run the Diagnostic Script

```bash
cd backend
python test_gemini.py
```

This will check:
- ✅ Gemini API key configuration
- ✅ Required libraries installation
- ✅ Schema file availability
- ✅ Snowflake credentials
- ✅ Live Gemini API connectivity

### Step 2: Check Backend Logs

Look at your terminal running the backend for detailed error messages:

```bash
# Terminal should show something like:
[INFO] Calling Gemini API for SQL generation...
[DEBUG] Raw Gemini Output: ...
[DEBUG] Cleaned SQL: ...
[INFO] Query executed successfully...
```

If you see `[ERROR]` messages, they will indicate the specific issue.

---

## 🔍 Common Issues & Solutions

### Issue 1: "GEMINI_API_KEY not found"

**Problem**: Environment variable is not set

**Solution**:
1. Make sure `.env` file exists in the `backend/` directory
2. Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   SNOWFLAKE_PASSWORD=your_snowflake_password
   ```
3. Restart the backend server

**Get API Key**:
- Go to: https://ai.google.dev
- Click "Get API Key"
- Create a new API key in Google Cloud console

---

### Issue 2: "Gemini API returned empty response"

**Problem**: The API is responding but returning nothing

**Possible Causes**:
- Model `gemini-2.5-flash` doesn't exist or isn't available
- API key has incorrect permissions
- Rate limiting

**Solution**:

Option A: Update to a different model version:

```python
# In backend/main.py, line ~167, change:
model='gemini-2.5-flash'
# To:
model='gemini-1.5-flash'
# Or:
model='gemini-pro'
```

Then restart the backend.

Option B: Check available models:
```bash
# Add this test in your test_gemini.py to list available models
client = genai.Client(api_key=api_key)
for model in client.models.list():
    print(model.name)
```

---

### Issue 3: "Invalid API Key" or "Permission Denied"

**Problem**: API key is not valid or doesn't have required permissions

**Solution**:
1. Go to https://ai.google.dev/
2. Sign in with the same Google account
3. Check that you enabled the Google AI API
4. Create a new API key and test it:
   ```bash
   python test_gemini.py
   ```

---

### Issue 4: "Failed to execute generated SQL on Snowflake"

**Problem**: SQL was generated but failed to execute

**Possible Causes**:
- Table or column names don't exist
- Snowflake credentials are incorrect
- Query syntax is invalid for Snowflake

**Solution**:
1. Look at the error message - it will show the generated SQL
2. Test the SQL directly in Snowflake:
   ```sql
   USE DATABASE NLP2SQL;
   USE SCHEMA TEST_SCHEMA;
   -- Paste the generated SQL here
   SELECT * FROM BALL_BY_BALL LIMIT 5;
   ```
3. Check if schema/tables exist in your Snowflake database
4. Verify SNOWFLAKE_PASSWORD in `.env` is correct

---

## 📋 Step-by-Step Troubleshooting

### 1. Restart Backend with Fresh Logs

```bash
# Kill the backend process (Ctrl+C in the terminal)
# Then restart it:
cd backend
python main.py
```

The startup should show:
```
======================================================================
🚀 DataGenie Core API Server Starting...
======================================================================
📍 Base URL: http://localhost:8000
📊 Query Endpoint: POST http://localhost:8000/api/query
❤️  Health Check: GET http://localhost:8000/health
```

### 2. Test Health Check

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "DataGenie Core API",
  "version": "1.0",
  "schema_loaded": true,
  "gemini_configured": true
}
```

### 3. Test Query with Simple Request

Try one of the suggested queries from the frontend:
- "Show me the top 10 batsmen with the most runs"
- "How many matches were played each season?"

### 4. Monitor Backend Output

Watch the backend terminal while executing a query. You should see:

```
============================================================
User Query: Show me the top 10 batsmen with the most runs
============================================================

[INFO] Calling Gemini API for SQL generation...
[DEBUG] Raw Gemini Output: SELECT BATTER, SUM(BATTER_RUNS) AS ...
[DEBUG] Cleaned SQL: SELECT BATTER, SUM(BATTER_RUNS) AS ...
[INFO] Executing SQL query...
[INFO] Query executed successfully. Returned 10 rows...
[SUCCESS] Query executed and returned 10 records
```

---

## 🔄 Full Restart Procedure

If the above doesn't work, do a complete restart:

```bash
# Terminal 1: Kill existing processes
# Press Ctrl+C in all terminals running frontend/backend

# Terminal 1: Backend
cd backend
pip install -r requirements.txt  # Make sure all packages installed
python main.py

# Terminal 2: Frontend (new terminal)
cd frontend
npm run dev
```

---

## 🧪 Testing in Detail

### Test 1: Verify API Key

```bash
# In the backend terminal, it should show on startup:
[INFO] Gemini API client initialized successfully (key length: 39 chars)
```

If this doesn't show, check your `.env` file.

### Test 2: Verify Schema is Loaded

Check that `IPL_SEMANTIC 4_8_2026, 1_30 AM (1).yaml` exists in the backend directory.

When backend starts, it should find this file.

### Test 3: Make a Manual API Call

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How many matches in total?"}'
```

The response should contain:
- `sql`: The generated SQL query
- `data`: The results array
- `columns`: Column names

---

## 💡 Pro Tips

1. **Check Frontend Error Details**: Look at the browser DevTools (F12) → Network tab → click the failed request → Response tab. The error message will be detailed.

2. **Backend Debug Mode**: The backend already logs everything. Just watch the terminal for `[DEBUG]`, `[INFO]`, `[ERROR]` messages.

3. **Model Compatibility**: If `gemini-2.5-flash` doesn't work, try `gemini-1.5-flash` or `gemini-pro`:
   
   ```python
   # In main.py line ~167
   model='gemini-1.5-flash'  # Change this
   ```

4. **Test Gemini Independently**: 
   ```python
   # Create a test file: backend/test_simple.py
   from google import genai
   from google.genai import types
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
   
   response = client.models.generate_content(
       model='gemini-2.5-flash',
       contents='Say hello'
   )
   print(response.text)
   ```
   
   Run: `python backend/test_simple.py`

---

## 📞 Need More Help?

1. **Check Logs**: Backend terminal has detailed error messages
2. **Run Diagnostic**: `python test_gemini.py` in backend directory
3. **Check .env**: Make sure both GEMINI_API_KEY and SNOWFLAKE_PASSWORD are set
4. **Verify Network**: Test `curl http://localhost:8000/health`
5. **Check Models**: Visit https://ai.google.dev/models to see available models

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ Health check returns healthy status
- ✅ Backend shows `[INFO] Calling Gemini API...` in logs
- ✅ Backend shows `[DEBUG] Raw Gemini Output: SELECT...`
- ✅ Frontend receives SQL, data, and columns
- ✅ Charts and tables render with results

---

**Last Updated**: May 2026 | **Version**: 1.0
