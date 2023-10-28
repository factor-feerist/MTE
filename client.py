import asyncio
try:
    import websockets.sync.client
except ImportError:
    import pip
    package = "websockets.sync.client"
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
    import websockets.sync.client

#виды команд:
#user open "file"
#user close
#user save "new name"
#user update
#user delete range
#user insert index text

with websockets.sync.client.connect("ws://localhost:8765") as ws:
        print("Connection opened")
        while True:
            cmd = input()
            ws.send(cmd)
            message = ws.recv()
            print(f"Received: {message}")
            if cmd == "log out":
<<<<<<< HEAD
                break
=======
                break
>>>>>>> 429acdc50b1c602403a591e9f55936e3dc067165
