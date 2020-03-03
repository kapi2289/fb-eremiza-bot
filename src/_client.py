import requests

from datetime import datetime
from time import sleep
from typing import List

from eremiza import Client as ERemizaClient
from eremiza._alarm import Alarm
from fbchat import Client as FbClient
from fbchat.models import ThreadType, Message, Mention, LocationAttachment

from ._settings import FB_GROUP_ID, TIMEZONE


class Client:
    eremiza_client: ERemizaClient
    client: FbClient
    alarms: List[Alarm]

    def __init__(self):
        self.alarms = list()
        self.client = None
        self.group_id = None
        self.wh_url = None

    def set_eremiza_client(self, client):
        self.eremiza_client = client

    def set_fbchat_client(self, client, group_id):
        self.client = client
        self.client.setDefaultThread(group_id, ThreadType.GROUP)
        self.group_id = group_id

    def set_dc_webhook_url(self, url):
        self.wh_url = url

    def listen(self):
        while self.eremiza_client and self.doOneListen():
            sleep(5)

    def doOneListen(self):
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
        if self.client:
            group = self.fetchGroupInfo(FB_GROUP_ID)[FB_GROUP_ID]
            mentions = [Mention(uid, offset=0, length=6) for uid in group.participants]
            message = Message(text=msg, mentions=mentions)
            if alarm.latitude and alarm.longitude:
                self.sendLocation(
                    LocationAttachment(alarm.latitude, alarm.longitude), message=message
                )
            else:
                self.send(message)
        
        if self.wh_url:
            msg += "\n@everyone"
            data = {"content": msg}
            requests.post(self.wh_url, json=data)
