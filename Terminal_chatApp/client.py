import threading
from queue import Queue
import websocket

online_users = set()
message_queue = Queue()

def hello(name):
    uri = "ws://192.168.137.1:8765" # This is my personal IP address that's acting like a host
    connection = True
    ws = websocket.WebSocket()
    ws.connect(uri)
    online_users.add(ws)
    ws.send("{} just joined...".format(name))
    try:
        receive_thread = threading.Thread(target=receive_messages, args=(ws,))
        receive_thread.start()

        while connection:
            user_input = input()
            if user_input:
                broadcast("{}: {}".format(name, user_input))
    finally:
        online_users.remove(ws)
        ws.close()

def receive_messages(ws):
    try:
        while True:
            message = ws.recv()
            print(message)
    except websocket.WebSocketConnectionClosedException:
        print("Connection closed.")

def broadcast(message):
    if online_users:
        for client in online_users:
            client.send(message)

client_name = input("Enter your name: ")
hello_thread = threading.Thread(target=hello, args=(client_name,))
hello_thread.start()
