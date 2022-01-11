import socket
import requests
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()

URL = "https://gist.githubusercontent.com/erickedji/68802/raw/7264f2d232702b4013490a0b2f9286cfa1b817e3/quotes.txt"
CRT = "C:\\Users\\chetverikov_is\\Downloads\\s.pem"

class QuotesDownloader:
    def __init__(self, url) -> None:
        self.url = url

    def get_quote(self) -> str:
        r = requests.get(self.url, verify=CRT)

        quotes = r.text.split("\r\n\r\n")
        return random.choice(quotes)

quotes_downloader = QuotesDownloader(URL)

while True:
    print("Waiting accept...")
    client_socket, addr = server_socket.accept()
    print(f"\tConnection from {addr}")

    while True:
        print("\tWating for data from {addr}...")
        request = client_socket.recv(16)
        print("\tRecieved request:", request)

        if not request:
            "\tClient has been disconected"
            break
        else:
            "\tSending a quote to the client..."
            response = (quotes_downloader.get_quote() + "\n").encode()
            client_socket.send(response)

    client_socket.close()