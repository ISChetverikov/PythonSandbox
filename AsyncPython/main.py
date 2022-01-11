import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()

while True:
    print("Waiting accept...")
    client_socket, addr = server_socket.accept()
    print(f"\tConnection from {addr}")

    while True:
        print("\tWating for data from {addr}...")
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = 'Hi'.encode()
            client_socket.send(response)

    client_socket.close()