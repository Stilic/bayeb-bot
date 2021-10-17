def handle(cmd, data):
    if cmd == "hello":
        return {"type": "text", "content": "hello " + data["user"]}
