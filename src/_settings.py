import io
import json
import os

from dotenv import load_dotenv
from pytz import timezone


def is_true(v):
    return str(v).lower() in ("yes", "true", "1")


load_dotenv()

FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")
FB_USE_SESSION = is_true(os.getenv("FB_USE_SESSION"))
FB_SESSION_FILE = os.getenv("FB_SESSION_FILE")
FB_SESSION = None

FB_GROUP_ID = os.getenv("FB_GROUP_ID")

if FB_USE_SESSION:
    with io.open(FB_SESSION_FILE, encoding="utf-8") as f:
        FB_SESSION = json.loads(f.read())

EREMIZA_EMAIL = os.getenv("EREMIZA_EMAIL")
EREMIZA_PASSWORD = os.getenv("EREMIZA_PASSWORD")

TIMEZONE = timezone("Europe/Warsaw")
