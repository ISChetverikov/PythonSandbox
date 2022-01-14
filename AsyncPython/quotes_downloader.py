import requests
import random


class QuotesDownloader:
    URL = "https://gist.githubusercontent.com/erickedji/68802/raw/7264f2d232702b4013490a0b2f9286cfa1b817e3/quotes.txt"
    CRT = "C:\\Users\\chetverikov_is\\Downloads\\s.pem"

    def __init__(self, url=URL) -> None:
        self.url = url

    def get_quote(self) -> str:
        r = requests.get(self.url, verify=self.CRT)

        quotes = r.text.split("\r\n\r\n")
        return random.choice(quotes)
