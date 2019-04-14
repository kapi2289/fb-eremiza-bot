from fbchat import Client as FbClient
from fbchat.models import ThreadType

from ._settings import FB_GROUP_ID


class Client(FbClient):

    def __init__(self, email, password, session_cookies=None):
        super(Client, self).__init__(email, password, session_cookies=session_cookies)
        self.setDefaultThread(FB_GROUP_ID, ThreadType.GROUP)
