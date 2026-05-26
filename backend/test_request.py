import json
import urllib.request

url = 'http://localhost:8000/api/query'
payload = {"prompt": "Show me the top 10 batsmen with the most runs"}
headers = {'Content-Type': 'application/json'}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        status = resp.status
        body = resp.read().decode('utf-8')
        print(f"STATUS: {status}")
        print(body)
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
