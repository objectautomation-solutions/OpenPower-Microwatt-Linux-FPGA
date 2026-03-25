# Edge-Based GenAI Chat Assistant (Offline LLM)

## Overview
This project implements an **Edge AI Chat Assistant** where an FPGA device communicates with a locally hosted Large Language Model (LLM) using Ollama.
![alt text](image-1.png)
The system works completely offline and enables real-time AI responses without relying on cloud services.

---

## Features
- Offline AI (no internet required)
- FPGA-based input interface
- Local LLM using Ollama
- HTTP-based communication
- Low-latency responses

---

## Architecture

![alt text](image.png)

---

## Tech Stack
- Python (client)
- Ollama (LLM runtime)
- HTTP (urllib)
- FPGA (Buildroot Linux)

---

## How It Works

1. User enters a query on OpenPOWER Microwatt Linux FPGA
2. FPGA sends HTTP request to local server
3. Ollama processes query using LLM
4. Response is sent back to OpenPOWER Microwatt Linux FPGA
5. OpenPOWER Microwatt Linux FPGA displays the result

---

## Setup Instructions
### 1. Install Ollama
### curl -fsSL https://ollama.com/install.sh | sh
### 2. Pull a lightweight model
### ollama pull phi < Any SLM [Small Language Model] >
### 3. Then Create Files For Creating HTTPS Communication From Linux Host To OpenPOWER Microwatt Linux FPGA
### Files named bridge.py And Client.py
### 4. Now In Linux Host Run The Ollama 
### Using OLLAMA_HOST=0.0.0.0 ollama serve
### 5. And Now Go The OpenPOWER Microwatt Linux FPGA Interface And Run The Client File
### Python3 Client.py

---

## Codes
### bridge.py 
```
import serial
import requests

SERIAL_PORT = '<Insert the Serial_Port>'
BAUD_RATE = <Baud Rate>

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

print("Bridge Started...")

buffer = ""

while True:
    try:
        data = ser.read(1024).decode(errors='ignore')

        if data:
            buffer += data

            if "\n" in buffer:
                lines = buffer.split("\n")

                for line in lines[:-1]:
                    prompt = line.strip()

                    # ignore shell prompts
                    if not prompt or prompt.startswith("#") or prompt.startswith("-sh"):
                        continue

                    print("FPGA:", prompt)

                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "<SLM_Model_Name>",
                            "prompt": prompt,
                            "stream": False
                        }
                    )

                    reply = response.json().get("response", "")

                    print("AI:", reply[:100])

                    ser.write((reply + "\n").encode())

                buffer = lines[-1]

    except Exception as e:
        print("Error:", e)

```

### Client.py

```
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

```


