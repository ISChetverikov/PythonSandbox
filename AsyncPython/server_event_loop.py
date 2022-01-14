import socket
from select import select
from quotes_downloader import QuotesDownloader

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()

quotes_downloader = QuotesDownloader()

def accept_connection(server_socket):
    print("Accepting...")
    client_socket, addr = server_socket.accept()
    print(f"\tConnection from {addr}")

    return client_socket

def respond_to_client(client_socket):
    print("\Recieving data from {client_socket.getsockname()}...")
    request = client_socket.recv(8)
    print("\tRecieved request:", request)

    if not request:
        print("\tClient has been disconected")
        client_socket.close()

        return True
    else:
        print("\tSending a quote to the client...")
        response = (quotes_downloader.get_quote() + "\n").encode()
        client_socket.send(response)

        return False

def event_loop():
    monitor_list = [ server_socket ]

    while True:

        print("Waiting for select...")
        ready_to_read, _, _ = select(monitor_list, [], [])

        for sock in ready_to_read:
            if sock is server_socket:
                client_socket = accept_connection(server_socket)
                monitor_list.append(client_socket)
            else:
                is_closed = respond_to_client(sock)

                if is_closed:
                    monitor_list.remove(sock)
    

if __name__ == "__main__":
    event_loop()
            