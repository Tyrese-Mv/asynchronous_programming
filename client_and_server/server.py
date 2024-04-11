import websockets
import asyncio

connected_clients = set()

async def echo(websocket, path):
    connected_clients.add(websocket)  # Add the current client to the set of connected clients
    print(connected_clients)
    
    try:
        async for message in websocket:
            # Send the received message to all other connected clients
            
            for client in connected_clients:
                if client != websocket:
                    print("message sent: {}".format(message))
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedError as e:
        print("Connection closed for {}: {}".format(websocket.remote_address, e))
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(echo, "0.0.0.0", 8765, ping_timeout=1000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()