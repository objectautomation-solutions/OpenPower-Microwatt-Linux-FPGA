import urllib.request
import json

URL = "http://<Local_Systen_IP>:11434/api/generate"

print("AI Chat Started...")

while True:
    user = input("You: ")

    data = json.dumps({
        "model": "<SLM_Model_Name>",
        "prompt": user,
        "stream": False
    }).encode('utf-8')

    req = urllib.request.Request(
        URL,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read().decode()


            first_json = raw.split('\n')[0]

            result = json.loads(first_json)

            print("AI:", result.get("response", ""))

    except Exception as e:
        print("Error:", e)
