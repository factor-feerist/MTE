import asyncio
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

async def handler(websocket, path):
    print("Client connected")
    while True:
        message = await websocket.recv()
        if len(message) > 5 and message[:5] == 'login':
            user = message[6:]
        else:
            await websocket.send("Вы ещё не залогинились!")
            continue
        async with lock:
            if user not in sockets.keys():
                sockets[user] = websocket
                await websocket.send("Вы залогинились!")
                break
            else:
                await websocket.send("Имя занято")

    while True:
        message = await websocket.recv()
        #await websocket.send(f"{command}!")
        if len(message) > 4 and message[:4] == 'open':
            #спрашиваем у файл хендлера есть ли файл и передаем содержимое
            await websocket.send(f"OK")
        if len(message) > 3 and message[:3] == 'new':
            #создаем новый файл
            await websocket.send(f"OK")
        #file_handler.parse_command(command)
        #по всем пользователям из файла сеансов, работающих над этим файлом отправить новую версию файла
        if len(message) >= 6 and message[:6] == 'logout':
            user = message[6:]
            await websocket.send(f"Пока, {user}!")
            break
        if "; pos [" in message:
            await manage_received_text_command(websocket, message)

    async with lock:
        del sockets[user]

async def manage_received_text_command(websocket, command):
    print(f"Processed command: {command}")

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
