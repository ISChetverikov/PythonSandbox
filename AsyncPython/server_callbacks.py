import socket
import selectors
from quotes_downloader import QuotesDownloader

selector = selectors.DefaultSelector()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    selector.register(server_socket, selectors.EVENT_READ, accept_connection)

quotes_downloader = QuotesDownloader()

def accept_connection(server_socket):
    print("Accepting...")
    client_socket, addr = server_socket.accept()
    print(f"\tConnection from {addr}")

    selector.register(client_socket, selectors.EVENT_READ, respond_to_client)

def respond_to_client(client_socket):
    print("\Recieving data from {client_socket.getsockname()}...")
    request = client_socket.recv(8)
    print("\tRecieved request:", request)

    if not request:
        print("\tClient has been disconected")
        selector.unregister(client_socket)

        return True
    else:
        print("\tSending a quote to the client...")
        response = (quotes_downloader.get_quote() + "\n").encode()
        client_socket.send(response)

        return False

def event_loop():

    while True:
        events = selector.select()
        for key, _ in events:
            key.data(key.fileobj)

if __name__ == "__main__":
    server()
    event_loop()
            