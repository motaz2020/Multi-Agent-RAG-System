import httpx

API = "http://127.0.0.1:8000/chat"
THREAD = "cli-default"

print("Smart Restaurant Assistant (Ctrl+C to exit)\n")
while True:
    try:
        msg = input("> ")
        if not msg.strip():
            continue
        r = httpx.post(API, json={"message": msg, "thread_id": THREAD}, timeout=120)
        data = r.json()
        print(f"\n{data.get('response', data.get('detail', 'Error'))}\n")
    except KeyboardInterrupt:
        print()
        break
    except Exception as e:
        print(f"Error: {e}\n")
