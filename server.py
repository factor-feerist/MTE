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
        user = await websocket.recv()
        async with lock:
            if user not in sockets.keys():
                sockets[user] = websocket
                await websocket.send("Вы залогинились!")
                break
            else:
                await websocket.send("Имя занято")
                
    while True:    
        command = await websocket.recv()
        await websocket.send(f"{command}!")
        #file_handler.parse_command(command)
        if command == "log out":
            await websocket.send(f"Пока, {user}!")
            break

    async with lock:
        del sockets[user]
     
start_server = websockets.serve(handler, "localhost", 8765)
 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
