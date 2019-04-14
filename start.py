from eremiza import Client as ERemizaClient

from src._client import Client
from src._settings import FB_EMAIL, FB_PASSWORD, FB_SESSION, EREMIZA_EMAIL, EREMIZA_PASSWORD

if __name__ == "__main__":
    client = Client(FB_EMAIL, FB_PASSWORD, session_cookies=FB_SESSION)
    client.set_eremiza_client(ERemizaClient(EREMIZA_EMAIL, EREMIZA_PASSWORD))
    client.listen()
