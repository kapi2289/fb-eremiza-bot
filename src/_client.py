from datetime import datetime
from time import sleep
from typing import List

from eremiza import Client as ERemizaClient
from eremiza._alarm import Alarm
from fbchat import Client as FbClient
from fbchat.models import ThreadType, Message, Mention, LocationAttachment

from ._settings import FB_GROUP_ID, TIMEZONE


class Client(FbClient):
    eremiza_client: ERemizaClient
    alarms: List[Alarm]

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
        ids = list(map(lambda a: a.id, self.alarms))
        alarms: List[Alarm] = self.eremiza_client.get_alarms(count=10)
        now = datetime.now(TIMEZONE).replace(tzinfo=None)

        for alarm in alarms:
            if alarm.id not in ids:
                self.alarms.append(alarm)
                if alarm.acquired <= now <= alarm.expiration:
                    self.alarm(alarm)

        return True

    def alarm(self, alarm: Alarm):
        msg = (
            "ALARM!\n"
            "Adres: {}\n"
            "Rodzaj: {}\n"
            "Opis: {}\n"
            "Dysponowano: {}\n".format(
                alarm.address,
                alarm.sub_kind,
                alarm.description,
                alarm.dispatched_bsis_name,
            )
        )
        group = self.fetchGroupInfo(FB_GROUP_ID)[FB_GROUP_ID]
        mentions = [Mention(uid, offset=0, length=6) for uid in group.participants]
        message = Message(text=msg, mentions=mentions)
        if alarm.latitude and alarm.longitude:
            self.sendLocation(
                LocationAttachment(alarm.latitude, alarm.longitude), message=message
            )
        else:
            self.send(message)
