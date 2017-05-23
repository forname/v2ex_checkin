# -*- coding: utf-8 -*-
import logging
import traceback

from apscheduler.schedulers.blocking import BlockingScheduler

from config import Config
from utils import send_mail, login, check_in

logging.basicConfig(format='%(asctime)s %(name)-12s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='v2ex.log',
                    filemode='w',
                    level=logging.WARNING)


def main():
    try:
        session = login(username=Config.V2EX_USERNAME, password=Config.V2EX_PASSWORD)
        login_msg, reward, balance = check_in(session)
    except:
        ex = traceback.format_exc()
        send_mail(ex=ex)
    else:
        logging.warning('{login_msg}, {reward}, {balance}'
                        .format(login_msg=login_msg, reward=reward, balance=balance))


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', hour=24)  # 定时任务

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print('bye bye...')
