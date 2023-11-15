import asyncio
from file_handler import FileHandler
try:
    import websockets
except ImportError:
    import pip
    package = "websockets"
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
    import websockets

lock = asyncio.Lock()
sockets = {}
f_handler = FileHandler()


async def login_user(websocket):
    while True:
        message = await websocket.recv()
        if message[:2] == 'l ':
            user = message[2:]
        else:
            await websocket.send("Вы ещё не залогинились!")
            continue
        async with lock:
            if user not in sockets.keys():
                sockets[user] = websocket
                await websocket.send("Вы залогинились!")
                return user
            else:
                await websocket.send("Имя занято")
        


async def handler(websocket, path):
    """Принимает команты вида 'ccd+', где cc - имя команды"""
    print("Client connected")
    user = await login_user(websocket)

    while True:
        message = await websocket.recv()
        #await websocket.send(f"{command}!")
        
        if message[:2] == 'o ':
            try:
                text = f_handler.open(message[2:], user)
                await websocket.send(f"OK")
                await websocket.send(text)
            except Exception as e:
                await websocket.send(str(e))

        elif message[:2] == 'n ':
            try:
                f_handler.new(message[2:], user)
                await websocket.send(f"OK")
            except Exception as e:
                await websocket.send(str(e))

        elif message[:2] == 'a ':
            ops = message[2:].split()
            filename = ops[0]
            text = f_handler.add(ops)
            for u in f_handler.get_users_by_filename(filename):
                await sockets[u].send(text)

        elif message[:2] == 'r ':
            ops = message[2:].split()
            filename = ops[0]
            text = f_handler.remove(ops)
            for u in f_handler.get_users_by_filename(filename):
                if u != user:
                    await sockets[u].send(text)

        elif message[:2] == 'w ':
            text = f_handler.watch(message[2:].split())

        elif message[:2] == 'lo':
            await websocket.send(f"Пока, {user}!")
            break

        #if "; pos [" in message:
            #await manage_received_text_command(websocket, message)

    async with lock:
        del sockets[user]

async def manage_received_text_command(websocket, command):
    print(f"Processed command: {command}")

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
