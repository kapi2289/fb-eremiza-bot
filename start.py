from eremiza import Client as ERemizaClient
from fbchat import Client as FbClient
from nexmo import Client as Nexmo

from src.client import Client
from src.settings import (
    FB_EMAIL,
    FB_PASSWORD,
    FB_SESSION,
    FB_GROUP_ID,
    EREMIZA_EMAIL,
    EREMIZA_PASSWORD,
    DISCORD_WEBHOOK_URL,
    NEXMO_ACTIVE,
    NEXMO_APP_ID,
)

if __name__ == "__main__":
    client = Client()
    if ((FB_EMAIL and FB_PASSWORD) or FB_SESSION) and FB_GROUP_ID:
        client.set_fbchat_client(
            FbClient(FB_EMAIL, FB_PASSWORD, session_cookies=FB_SESSION)
        )
    if DISCORD_WEBHOOK_URL:
        client.set_dc_webhook_url(DISCORD_WEBHOOK_URL)
    if NEXMO_ACTIVE:
        client.set_nexmo_client(
            Nexmo(application_id=NEXMO_APP_ID, private_key="private.key")
        )
    client.set_eremiza_client(ERemizaClient(EREMIZA_EMAIL, EREMIZA_PASSWORD))
    client.listen()
