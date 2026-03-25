import serial
import requests

SERIAL_PORT = '<Insert the Serial_Port>'
BAUD_RATE = '<Baud Rate>'

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
