import socket
from select import select
from quotes_downloader import QuotesDownloader

quotes_downloader = QuotesDownloader()

tasks = []
to_read = {}
to_write = {}

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    while True:
        yield('read', 'server_accept',  server_socket)
        print("Accepting...")
        client_socket, addr = server_socket.accept()
        print(f"\tConnection from {addr}")

        tasks.append(client(client_socket))

def client(client_socket):

    while True:
        yield ("read", "client_recv", client_socket)
        print("\Recieving data from {client_socket.getsockname()}...")
        request = client_socket.recv(8)
        print("\tRecieved request:", request)

        if not request:
            print("\tClient has been disconected")
            break

        else:
            yield ('write', "client_send", client_socket)
            print("\tSending a quote to the client...")
            response = (quotes_downloader.get_quote() + "\n").encode()
            client_socket.send(response)

    client_socket.close()

def event_loop():

    while True:

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            reason, msg, sock = next(task)
            print(f"What to waiting: {msg}")

            if reason == "read":
                to_read[sock] = task

            if reason == "write":
                to_write[sock] = task

        except StopIteration:
            print("I'm Done")

tasks.append(server())
event_loop()
            