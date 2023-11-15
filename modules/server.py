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
    try:
        user = None
        user = await login_user(websocket)

        while True:
            message = await websocket.recv()
            
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

            elif message[:2] == 's ':
                try:
                    version = f_handler.save(message[2:])
                    await websocket.send(f"OK")
                    await websocket.send(f"Version {version} of file {message[2:]} was saved")
                except Exception as e:
                    await websocket.send(str(e))

            elif message[:2] == 'a ':
                ops = message[2:].split('\\\\')
                filename = ops[0]
                text = f_handler.add(*ops)
                for u in f_handler.get_users_by_filename(filename):
                    if u != user:
                        await sockets[u].send(text)

            elif message[:2] == 'r ':
                ops = message[2:].split('\\\\')
                filename = ops[0]
                text = f_handler.remove(*ops)
                for u in f_handler.get_users_by_filename(filename):
                    if u != user:
                        await sockets[u].send(text)

            elif message[:2] == 'w ':
                try:
                    text = f_handler.watch(*message[2:].split())
                    await websocket.send('OK')
                    await websocket.send(text)
                except Exception as e:
                    await websocket.send(str(e))

            elif message[:2] == 'wl':
                try:
                    text = f_handler.get_log_by_filename(message[2:])
                    await websocket.send('OK')
                    await websocket.send(text)
                except Exception as e:
                    await websocket.send(str(e))

            elif message[:2] == 'lo':
                await websocket.send(f"Пока, {user}!")
                break

            elif message[:2] == 'c ':
                try:
                    version = f_handler.remove_user_from_files(message[2:])
                    await websocket.send(f"OK")
                    await websocket.send(f"File was closed")
                except Exception as e:
                    await websocket.send(str(e))

        async with lock:
            del sockets[user]
        f_handler.remove_user_from_files(user)

    except websockets.exceptions.ConnectionClosedError:
        if user is not None:
            async with lock:
                del sockets[user]
            f_handler.remove_user_from_files(user)
        print("Client disconnected")

start_server = websockets.serve(handler, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
