from datetime import datetime
from time import sleep

from eremiza import Client as ERemizaClient
from fbchat import Client as FbClient
from fbchat.models import ThreadType, Message, Mention

from ._settings import FB_GROUP_ID, TIMEZONE


class Client(FbClient):
    eremiza_client: ERemizaClient
    alarms: list

    def __init__(self, email, password, session_cookies=None):
        super(Client, self).__init__(email, password, session_cookies=session_cookies)
        self.alarms = list()
        self.setDefaultThread(FB_GROUP_ID, ThreadType.GROUP)

    def set_eremiza_client(self, client):
        self.eremiza_client = client

    def listen(self, **kwargs):
        self.startListening()
        self.onListening()

        while self.listening and self.doOneListen():
            sleep(5)

        self.stopListening()

    def doOneListen(self, **kwargs):
        ids = list(map(lambda a: a["id"], self.alarms))
        alarms = self.eremiza_client.get_alarms(count=10)
        now = datetime.now(TIMEZONE)

        for alarm in alarms:
            acquired, expiration = list(
                map(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=TIMEZONE),
                    (alarm["aquired"], alarm["expiration"])))
            if alarm["id"] not in ids:
                self.alarms.append(alarm)
                if acquired <= now <= expiration:
                    self.alarm(alarm)

        return True

    def alarm(self, alarm):
        msg = "ALARM!\nRodzaj: {subKind}\nOpis: {description}\nDysponowano: {dispatchedBsisName}".format(**alarm)
        group = self.fetchGroupInfo(FB_GROUP_ID)[FB_GROUP_ID]
        mentions = [Mention(uid, offset=0, length=6) for uid in group.participants]
        self.send(Message(text=msg, mentions=mentions))
