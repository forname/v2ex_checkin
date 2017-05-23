# -*- coding: utf-8 -*-
import smtplib
import requests
import re

from bs4 import BeautifulSoup
from email.mime.text import MIMEText

from config import Config


def send_mail(ex):
    """
    send mail
    
    :param ex: 异常信息
    :return: 
    """
    msg = MIMEText(ex, _subtype='plain', _charset='utf-8')
    msg['Subject'] = Config.MAIL_SUBJECT_PREFIX
    msg['From'] = Config.MAIL_USERNAME
    msg['To'] = Config.MAIL_USERNAME

    if Config.MAIL_USE_SSL:
        server = smtplib.SMTP_SSL(Config.MAIL_SERVER, Config.MAIL_PORT)
    else:
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
    server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    server.sendmail(Config.MAIL_USERNAME, [Config.MAIL_USERNAME], msg.as_string())
    server.close()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Referer": "http://cn.v2ex.com/signin",
    "Origin": "http://cn.v2ex.com",
    "Host": "cn.v2ex.com"
}


def login(username, password):
    """ login """
    url = "http://cn.v2ex.com/signin"
    session = requests.session()
    resp = session.get(url=url)
    soup = BeautifulSoup(resp.text, "html.parser")
    inputs = soup.find_all("input")

    params = {
        inputs[1]["name"]: username,
        inputs[2]["name"]: password,
        inputs[3]["name"]: inputs[3]["value"],
        inputs[5]["name"]: inputs[5]["value"]
    }

    resp = session.post(url=url, params=params, headers=headers)
    return session


def check_in(session):
    """ 签到 """
    headers['Referer'] = "http://cn.v2ex.com/"
    resp = session.get(url='https://www.v2ex.com/mission/daily', headers=headers)
    login_msg = re.findall(r'已连续登录 \d+ 天', resp.text)[0]

    resp = session.get(url='https://cn.v2ex.com/balance', headers=headers)
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")
    data_table = soup.find("table", class_="data")
    tr = data_table.find_all("tr")[1]
    tds = tr.find_all("td")
    reward = tds[2].get_text()
    balance = tds[3].get_text()
    return login_msg, reward, balance
