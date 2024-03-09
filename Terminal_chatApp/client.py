import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError
from asyncio import Queue

online_users = set()
message_queue = Queue()

async def hello(name):
    uri = "ws://192.168.18.68:8765" # This is my personal IP address that's acting like a host
    connection = True
    async with websockets.connect(uri) as websocket:
        online_users.add(websocket)
        print(online_users)
        try:
            listen_task = asyncio.create_task(receive_messages(websocket, name))
            while connection:
                while not message_queue.empty():
                    message = await message_queue.get()
                    print(message)
                user_input = input()
                if user_input:
                    await broadcast("{}: {}".format(name, user_input))
            listen_task.cancel()
        finally:
            online_users.remove(websocket)

async def receive_messages(websocket, name):
    try:
        while True:
            message = await websocket.recv()
            await message_queue.put(message)
    except ConnectionClosedError:
        print("Connection closed.")

async def broadcast(message):
    if online_users:
        coroutines = [client.send(message) for client in online_users]
        await asyncio.gather(*coroutines)

client_name = input("Enter your name: ")
asyncio.get_event_loop().run_until_complete(hello(client_name))