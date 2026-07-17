import httpx
import json

url = "http://localhost:8000/chat/"
data = {
    "query": "hi, i am shanky",
    "user_id": "test_user",
    "thread_id": "test_thread_123"
}

with httpx.stream("POST", url, json=data, timeout=60.0) as r:
    for line in r.iter_lines():
        if line:
            print("Received:", line)
