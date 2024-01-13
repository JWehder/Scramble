import requests

class Base:
    
    def __init__(self) -> None:
        pass

    def fetch_data(self, url):
        return requests.get(url)
