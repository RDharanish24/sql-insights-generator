#!/usr/bin/env python3
"""
Diagnostic script to test Gemini API configuration and connectivity.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("\n" + "="*70)
print("🔍 DataGenie Core - Gemini API Diagnostic Tool")
print("="*70 + "\n")

# Check 1: API Key
print("1️⃣  Checking Gemini API Key...")
api_key = os.environ.get('GEMINI_API_KEY')
if api_key:
    print(f"   ✅ GEMINI_API_KEY found (length: {len(api_key)} chars)")
    print(f"   🔑 Key preview: {api_key[:10]}...{api_key[-10:]}")
else:
    print("   ❌ GEMINI_API_KEY not found in environment!")
    print("   💡 Make sure GEMINI_API_KEY is set in your .env file")
    sys.exit(1)

# Check 2: Required libraries
print("\n2️⃣  Checking required Python libraries...")
required_libs = {
    'google.genai': 'google-genai',
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn',
    'snowflake.connector': 'snowflake-connector-python',
    'yaml': 'pyyaml',
}

for module, package in required_libs.items():
    try:
        __import__(module)
        print(f"   ✅ {package} installed")
    except ImportError:
        print(f"   ❌ {package} NOT installed")
        print(f"      Install with: pip install {package}")

# Check 3: Schema file
print("\n3️⃣  Checking schema file...")
schema_file = "IPL_SEMANTIC 4_8_2026, 1_30 AM (1).yaml"
if os.path.exists(schema_file):
    size = os.path.getsize(schema_file)
    print(f"   ✅ Schema file found ({size} bytes)")
else:
    print(f"   ❌ Schema file '{schema_file}' not found")
    print(f"   💡 Make sure the schema file is in the backend directory")

# Check 4: Snowflake credentials
print("\n4️⃣  Checking Snowflake credentials...")
sf_password = os.environ.get('SNOWFLAKE_PASSWORD')
if sf_password:
    print(f"   ✅ SNOWFLAKE_PASSWORD found (length: {len(sf_password)} chars)")
else:
    print("   ❌ SNOWFLAKE_PASSWORD not found")
    print("   💡 Make sure SNOWFLAKE_PASSWORD is set in your .env file")

# Check 5: Test Gemini API connection
print("\n5️⃣  Testing Gemini API connection...")
try:
    from google import genai
    from google.genai import types
    
    print("   📡 Initializing Gemini client...")
    client = genai.Client(api_key=api_key)
    print("   ✅ Gemini client initialized successfully")
    
    print("   📡 Testing API with a simple prompt...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="What is 2 + 2? Answer in one word.",
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=100
        )
    )
    
    if response and hasattr(response, 'text') and response.text:
        print(f"   ✅ API response received: '{response.text.strip()}'")
        print("\n   🎉 Gemini API is working correctly!")
    else:
        print(f"   ❌ API returned empty response")
        print(f"      Response object: {response}")
        
except Exception as e:
    print(f"   ❌ Gemini API test failed!")
    print(f"      Error Type: {type(e).__name__}")
    print(f"      Error Message: {str(e)}")
    print(f"\n   💡 Common issues:")
    print(f"      • Invalid API key")
    print(f"      • API key doesn't have required permissions")
    print(f"      • Network connectivity issue")
    print(f"      • Model name 'gemini-2.5-flash' may not be available")
    print(f"\n   🔧 Troubleshooting:")
    print(f"      1. Verify your API key at: https://ai.google.dev")
    print(f"      2. Check available models: https://ai.google.dev/models")
    print(f"      3. Try 'gemini-1.5-flash' if 2.5 is not available")

print("\n" + "="*70)
print("Diagnostic complete!")
print("="*70 + "\n")
