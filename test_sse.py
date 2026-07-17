import httpx
import json

def test_stream():
    url = "http://127.0.0.1:8000/chat/"
    payload = {"query": "hi", "user_id": "test"}
    
    with httpx.stream("POST", url, json=payload) as r:
        print("Status Code:", r.status_code)
        for chunk in r.iter_raw():
            if chunk:
                print(chunk.decode("utf-8"), end="")

if __name__ == "__main__":
    test_stream()
