# -*-coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from database import Session
from sqlalchemy.exc import ProgrammingError, IntegrityError

from analyser.utility import InvalidInfoException, http_request_filter
from .model import Auction

session = Session()


@http_request_filter(".*auction.co.kr")
def handler(req):
    try:
        auction_crawling(req.cookie)
    except InvalidInfoException:
        return


def auction_crawling(cookie_dict):
    jar = requests.cookies.RequestsCookieJar()

    for key in cookie_dict:
        jar.set(key, cookie_dict[key])

    url = 'https://memberssl.auction.co.kr/membership/MyInfo/MyInfo.aspx'
    request = requests.get(url, cookies=jar, verify=False)

    data = request.content
    soup = BeautifulSoup(data, "lxml")

    userid = soup.find('span', attrs={'id': 'lblMemberId'})
    username = soup.find('span', attrs={'id': 'lblMemberName'})
    if userid is None or username is None:
        return
    user_name = username.text
    user_id = userid.text

    ip_line2 = soup.findAll('td', attrs={'class': 'ip line2'})

    address = ip_line2[0].findAll('input')

    address_2 = address[1]['value']
    address_3 = address[2]['value']

    ddl_home_tel = soup.findAll('select', attrs={'name': 'ddlHomeTel'})
    ddl_home_tel = ddl_home_tel[0].findAll('option', attrs={'selected': 'selected'})
    home_tel_1 = ddl_home_tel[0]['value']

    info = soup.findAll('div', attrs={'class': 'input1'})

    txt_home_tel2 = info[0].findAll('input', attrs={'name': 'txtHomeTel2'})
    txt_home_tel3 = info[1].findAll('input', attrs={'name': 'txtHomeTel3'})
    txt_mobile_tel2 = info[2].findAll('input', attrs={'name': 'txtMobileTel2'})
    txt_mobile_tel3 = info[3].findAll('input', attrs={'name': 'txtMobileTel3'})

    home_tel_2 = txt_home_tel2[0]['value']
    home_tel_3 = txt_home_tel3[0]['value']
    mobile_tel_2 = txt_mobile_tel2[0]['value']
    mobile_tel_3 = txt_mobile_tel3[0]['value']

    ddl_mobile_tel = soup.findAll('select', attrs={'name': 'ddlMobileTel'})
    ddl_mobile_tel = ddl_mobile_tel[0].findAll('option', attrs={'selected': 'selected'})

    mobile_tel_1 = ddl_mobile_tel[0]['value']

    txt_email_id = info[4].findAll('input', attrs={'name': 'txtEmailId'})
    txt_email_domain = info[5].findAll('input', attrs={'name': 'txtEmailDomain'})

    email_id = txt_email_id[0]['value']
    email_domain = txt_email_domain[0]['value']

    tel_home = home_tel_1 + "-" + home_tel_2 + "-" + home_tel_3
    tel_mobile = mobile_tel_1 + "-" + mobile_tel_2 + "-" + mobile_tel_3
    email = email_id + "@" + email_domain
    address = address_2 + address_3

    session.add(Auction(user_name, user_id, tel_home, tel_mobile, email, address))
    try:
        session.commit()
    except (ProgrammingError, IntegrityError):
        session.rollback()
