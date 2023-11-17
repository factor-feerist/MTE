import sys
import asyncio
from modules.file_handler import FileHandler
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


async def handler(websocket, _path):
    """Принимает команты вида 'ccd+', где cc - имя команды"""
    print("Client connected")
    user = None
    try:
        user = await login_user(websocket)
        filename = None

        while True:
            message = await websocket.recv()
            
            if message[:2] == 'o ':
                try:
                    filename = message[2:]
                    text = f_handler.open(filename, user)
                    await websocket.send(f"OK")
                    await websocket.send(text)
                except Exception as e:
                    await websocket.send(str(e))

            elif message[:2] == 'n ':
                try:
                    filename = message[2:]
                    f_handler.new(filename, user)
                    await websocket.send(f"OK")
                except Exception as e:
                    await websocket.send(str(e))

            elif message[:2] == 's ':
                try:
                    ops = message[2:].split()
                    version = f_handler.save(*ops)
                    await websocket.send(f"OK")
                    await websocket.send(
                        f"Version {version} of file {ops[0]} was saved")
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
                    f_handler.remove_user_from_files(message[2:])
                    await websocket.send(f"OK")
                    await websocket.send(f"File {filename} was closed")
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


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
